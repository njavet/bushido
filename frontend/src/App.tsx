import './App.css'
import { LogEntryForm } from "./components/LogEntryForm.tsx";
import { UnitLogsBrowser} from "./components/UnitLogsBrowser.tsx";
import { UnitSettingsPanel} from "./components/UnitSettingsPanel.tsx";

function App() {
  return (
    <>
      <LogEntryForm/>
      <UnitLogsBrowser/>
      <UnitSettingsPanel/>
    </>
  )
}

export default App
