module Main exposing (main)

import Browser
import Html exposing (Html, button, div, form, h1, input, label, span, text)
import Html.Attributes exposing (autocomplete, class, disabled, placeholder, type_, value)
import Html.Events exposing (onInput, onSubmit)
import Http
import Json.Decode as Decode exposing (Decoder, Value)
import Json.Encode as Encode
import String


type alias Flags =
    { apiBaseUrl : String }


type alias Model =
    { apiBaseUrl : String
    , authMode : AuthMode
    , authState : AuthState
    , token : Maybe String
    , name : String
    , email : String
    , password : String
    , command : String
    , output : List TerminalEntry
    }


type AuthMode
    = LoginMode
    | SignupMode


type AuthState
    = LoggedOut
    | Authenticating
    | LoadingIdentity
    | LoggedIn Spartan
    | AuthFailed String


type alias Spartan =
    { id : Int
    , name : String
    , email : String
    , isActive : Bool
    , isAdmin : Bool
    }


type alias Token =
    { accessToken : String }


type TerminalEntry
    = CommandEntry String
    | InfoEntry String
    | ErrorEntry String
    | UnitEntry Value
    | UnitListEntry (List Value)


type Msg
    = SetName String
    | SetEmail String
    | SetPassword String
    | SetCommand String
    | SwitchAuthMode
    | SubmitAuth
    | AuthCompleted (Result Http.Error Token)
    | MeCompleted (Result Http.Error Spartan)
    | SubmitCommand
    | LogCompleted (Result Http.Error Value)
    | LoadCompleted (Result Http.Error (List Value))
    | Logout


main : Program Flags Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = \_ -> Sub.none
        , view = view
        }


init : Flags -> ( Model, Cmd Msg )
init flags =
    ( { apiBaseUrl = String.trimRight flags.apiBaseUrl
      , authMode = LoginMode
      , authState = LoggedOut
      , token = Nothing
      , name = ""
      , email = ""
      , password = ""
      , command = ""
      , output = []
      }
    , Cmd.none
    )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        SetName name ->
            ( { model | name = name }, Cmd.none )

        SetEmail email ->
            ( { model | email = email }, Cmd.none )

        SetPassword password ->
            ( { model | password = password }, Cmd.none )

        SetCommand command ->
            ( { model | command = command }, Cmd.none )

        SwitchAuthMode ->
            ( { model
                | authMode =
                    case model.authMode of
                        LoginMode ->
                            SignupMode

                        SignupMode ->
                            LoginMode
                , authState = LoggedOut
              }
            , Cmd.none
            )

        SubmitAuth ->
            if String.isEmpty (String.trim model.email) || String.isEmpty model.password then
                ( { model | authState = AuthFailed "Email and password are required." }, Cmd.none )

            else
                ( { model | authState = Authenticating }, authenticate model )

        AuthCompleted result ->
            case result of
                Ok token ->
                    ( { model
                        | token = Just token.accessToken
                        , authState = LoadingIdentity
                        , password = ""
                      }
                    , getMe model.apiBaseUrl token.accessToken
                    )

                Err err ->
                    ( { model | authState = AuthFailed (httpError err) }, Cmd.none )

        MeCompleted result ->
            case result of
                Ok spartan ->
                    ( { model
                        | authState = LoggedIn spartan
                        , output = [ InfoEntry ("IDENTITY VERIFIED // SPARTAN " ++ spartan.name) ]
                      }
                    , Cmd.none
                    )

                Err err ->
                    ( logoutModel model (httpError err), Cmd.none )

        SubmitCommand ->
            let
                raw =
                    String.trim model.command

                withCommand =
                    if String.isEmpty raw then
                        model

                    else
                        { model
                            | command = ""
                            , output = model.output ++ [ CommandEntry raw ]
                        }
            in
            if String.isEmpty raw then
                ( model, Cmd.none )

            else
                case model.token of
                    Nothing ->
                        ( logoutModel model "Authentication required.", Cmd.none )

                    Just token ->
                        runCommand token raw withCommand

        LogCompleted result ->
            case result of
                Ok unit ->
                    ( { model | output = model.output ++ [ InfoEntry "UNIT LOGGED", UnitEntry unit ] }, Cmd.none )

                Err err ->
                    handleAuthenticatedError err model

        LoadCompleted result ->
            case result of
                Ok units ->
                    ( { model
                        | output =
                            model.output
                                ++ [ InfoEntry ("LOAD COMPLETE // " ++ String.fromInt (List.length units) ++ " RECORDS")
                                   , UnitListEntry units
                                   ]
                      }
                    , Cmd.none
                    )

                Err err ->
                    handleAuthenticatedError err model

        Logout ->
            ( logoutModel model "SESSION CLOSED", Cmd.none )


runCommand : String -> String -> Model -> ( Model, Cmd Msg )
runCommand token raw model =
    case String.words raw of
        "log" :: rest ->
            let
                line =
                    String.join " " rest
            in
            if String.isEmpty line then
                ( appendError "Usage: log <unit line>" model, Cmd.none )

            else
                ( model, logUnit model.apiBaseUrl token line )

        "load" :: unitName :: [] ->
            ( model, loadUnits model.apiBaseUrl token unitName )

        "load" :: [] ->
            ( appendError "Usage: load <unit_name>" model, Cmd.none )

        _ ->
            ( appendError "Unknown command. Available: log, load" model, Cmd.none )


authenticate : Model -> Cmd Msg
authenticate model =
    let
        ( path, body ) =
            case model.authMode of
                LoginMode ->
                    ( "/api/auth/login"
                    , Encode.object
                        [ ( "email", Encode.string model.email )
                        , ( "password", Encode.string model.password )
                        ]
                    )

                SignupMode ->
                    ( "/api/auth/signup"
                    , Encode.object
                        [ ( "name", Encode.string model.name )
                        , ( "email", Encode.string model.email )
                        , ( "password", Encode.string model.password )
                        ]
                    )
    in
    Http.post
        { url = model.apiBaseUrl ++ path
        , body = Http.jsonBody body
        , expect = Http.expectJson AuthCompleted tokenDecoder
        }


getMe : String -> String -> Cmd Msg
getMe apiBaseUrl token =
    Http.request
        { method = "GET"
        , headers = authHeaders token
        , url = apiBaseUrl ++ "/api/auth/me"
        , body = Http.emptyBody
        , expect = Http.expectJson MeCompleted spartanDecoder
        , timeout = Nothing
        , tracker = Nothing
        }


logUnit : String -> String -> String -> Cmd Msg
logUnit apiBaseUrl token line =
    Http.request
        { method = "POST"
        , headers = authHeaders token
        , url = apiBaseUrl ++ "/api/unit/logs"
        , body = Http.jsonBody (Encode.object [ ( "line", Encode.string line ) ])
        , expect = Http.expectJson LogCompleted Decode.value
        , timeout = Nothing
        , tracker = Nothing
        }


loadUnits : String -> String -> String -> Cmd Msg
loadUnits apiBaseUrl token unitName =
    Http.request
        { method = "POST"
        , headers = authHeaders token
        , url = apiBaseUrl ++ "/api/unit/logs/query"
        , body =
            Http.jsonBody
                (Encode.object
                    [ ( "unit_name", Encode.string unitName )
                    , ( "start_t", Encode.null )
                    , ( "end_t", Encode.null )
                    ]
                )
        , expect = Http.expectJson LoadCompleted (Decode.list Decode.value)
        , timeout = Nothing
        , tracker = Nothing
        }


authHeaders : String -> List Http.Header
authHeaders token =
    [ Http.header "Authorization" ("Bearer " ++ token) ]


tokenDecoder : Decoder Token
tokenDecoder =
    Decode.map Token (Decode.field "access_token" Decode.string)


spartanDecoder : Decoder Spartan
spartanDecoder =
    Decode.map5 Spartan
        (Decode.field "id" Decode.int)
        (Decode.field "name" Decode.string)
        (Decode.field "email" Decode.string)
        (Decode.field "is_active" Decode.bool)
        (Decode.field "is_admin" Decode.bool)


handleAuthenticatedError : Http.Error -> Model -> ( Model, Cmd Msg )
handleAuthenticatedError err model =
    case err of
        Http.BadStatus 401 ->
            ( logoutModel model "SESSION EXPIRED // AUTHENTICATION REQUIRED", Cmd.none )

        _ ->
            ( appendError (httpError err) model, Cmd.none )


appendError : String -> Model -> Model
appendError message model =
    { model | output = model.output ++ [ ErrorEntry message ] }


logoutModel : Model -> String -> Model
logoutModel model message =
    { model
        | authState = LoggedOut
        , token = Nothing
        , password = ""
        , command = ""
        , output =
            if String.isEmpty message then
                []

            else
                [ InfoEntry message ]
    }


httpError : Http.Error -> String
httpError err =
    case err of
        Http.BadUrl _ ->
            "Invalid Citadel URL."

        Http.Timeout ->
            "Citadel request timed out."

        Http.NetworkError ->
            "Citadel is unreachable."

        Http.BadStatus status ->
            "Citadel returned HTTP " ++ String.fromInt status ++ "."

        Http.BadBody detail ->
            "Unexpected Citadel response: " ++ detail


view : Model -> Html Msg
view model =
    div [ class "app-shell" ]
        [ div [ class "scanline" ] []
        , case model.authState of
            LoggedIn spartan ->
                viewTerminal model spartan

            _ ->
                viewAuth model
        ]


viewAuth : Model -> Html Msg
viewAuth model =
    div [ class "auth-wrap" ]
        [ div [ class "auth-panel" ]
            [ div [ class "eyebrow" ] [ text "BUSHIDO // CITADEL" ]
            , h1 [] [ text "SECURE TERMINAL ACCESS" ]
            , div [ class "system-line" ]
                [ span [ class "status-dot offline" ] []
                , text " CITADEL NETWORK // DISCONNECTED"
                ]
            , form [ onSubmit SubmitAuth ]
                [ case model.authMode of
                    SignupMode ->
                        field "SPARTAN" "name" model.name SetName False

                    LoginMode ->
                        text ""
                , field "IDENTITY" "email" model.email SetEmail False
                , field "PASSPHRASE" "password" model.password SetPassword True
                , button
                    [ class "primary"
                    , type_ "submit"
                    , disabled (model.authState == Authenticating || model.authState == LoadingIdentity)
                    ]
                    [ text
                        (case model.authState of
                            Authenticating ->
                                "AUTHENTICATING..."

                            LoadingIdentity ->
                                "VERIFYING IDENTITY..."

                            _ ->
                                case model.authMode of
                                    LoginMode ->
                                        "AUTHENTICATE"

                                    SignupMode ->
                                        "CREATE SPARTAN"
                        )
                    ]
                ]
            , case model.authState of
                AuthFailed message ->
                    div [ class "auth-error" ] [ text ("[AUTH FAILED] " ++ message) ]

                _ ->
                    text ""
            , button [ class "link-button", type_ "button", Html.Events.onClick SwitchAuthMode ]
                [ text
                    (case model.authMode of
                        LoginMode ->
                            "NO IDENTITY // CREATE SPARTAN"

                        SignupMode ->
                            "EXISTING IDENTITY // LOGIN"
                    )
                ]
            ]
        ]


field : String -> String -> String -> (String -> Msg) -> Bool -> Html Msg
field caption hint currentValue toMsg secret =
    label [ class "field" ]
        [ span [] [ text caption ]
        , input
            [ type_
                (if secret then
                    "password"

                 else
                    "text"
                )
            , placeholder hint
            , value currentValue
            , onInput toMsg
            , autocomplete
                (if secret then
                    "current-password"

                 else
                    "off"
                )
            ]
            []
        ]


viewTerminal : Model -> Spartan -> Html Msg
viewTerminal model spartan =
    div [ class "terminal-frame" ]
        [ div [ class "terminal-header" ]
            [ div []
                [ div [ class "eyebrow" ] [ text "BUSHIDO // CITADEL" ]
                , div [ class "identity" ] [ text ("SPARTAN // " ++ String.toUpper spartan.name) ]
                ]
            , div [ class "header-actions" ]
                [ div [ class "system-line" ]
                    [ span [ class "status-dot online" ] []
                    , text " ONLINE"
                    ]
                , button [ class "link-button", Html.Events.onClick Logout ] [ text "LOGOUT" ]
                ]
            ]
        , div [ class "output" ] (List.map viewEntry model.output)
        , form [ class "command-line", onSubmit SubmitCommand ]
            [ span [ class "prompt" ] [ text "bushido>" ]
            , input
                [ class "command-input"
                , value model.command
                , onInput SetCommand
                , placeholder "log ... | load <unit_name>"
                , autocomplete "off"
                ]
                []
            ]
        ]


viewEntry : TerminalEntry -> Html Msg
viewEntry entry =
    case entry of
        CommandEntry command ->
            div [ class "entry command-entry" ]
                [ span [ class "prompt" ] [ text ">" ]
                , text (" " ++ command)
                ]

        InfoEntry message ->
            div [ class "entry info-entry" ] [ text ("[OK] " ++ message) ]

        ErrorEntry message ->
            div [ class "entry error-entry" ] [ text ("[ERROR] " ++ message) ]

        UnitEntry unit ->
            div [ class "entry json-entry" ] [ text (Encode.encode 2 unit) ]

        UnitListEntry units ->
            div []
                (List.indexedMap
                    (\index unit ->
                        div [ class "entry json-entry" ]
                            [ span [ class "record-index" ] [ text ("#" ++ String.fromInt (index + 1) ++ " ") ]
                            , text (Encode.encode 2 unit)
                            ]
                    )
                    units
                )
