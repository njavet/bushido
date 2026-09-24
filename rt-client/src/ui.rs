use chrono::{Datelike, Days, Local, NaiveDate};
use ratatui::{
    Frame,
    layout::{Constraint, Direction, Layout, Rect},
    style::{Modifier, Style},
    text::{Line, Span},
    widgets::{Block, Borders, Paragraph},
};

use crate::app::App;

const WEEKDAYS: [&str; 7] = [
    "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",
];

pub fn render(frame: &mut Frame, app: &App) {
    let area = frame.area();

    let rows = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),
            Constraint::Length(2),
            Constraint::Min(12),
            Constraint::Length(1),
        ])
        .split(area);

    render_header(frame, app, rows[0]);
    render_weekdays(frame, rows[1]);
    render_month(frame, app, rows[2]);
    render_help(frame, rows[3]);
}

fn render_header(frame: &mut Frame, app: &App, area: Rect) {
    let title = app.selected.format("%B %Y").to_string();

    let paragraph = Paragraph::new(Line::from(vec![
        Span::styled(
            title,
            Style::default().add_modifier(Modifier::BOLD),
        ),
        Span::raw("    "),
        Span::raw(format!(
            "Selected: {}",
            app.selected.format("%d %b %Y")
        )),
    ]))
        .block(
            Block::default()
                .title(" BUSHIDO ")
                .borders(Borders::ALL),
        );

    frame.render_widget(paragraph, area);
}

fn render_weekdays(frame: &mut Frame, area: Rect) {
    let columns = seven_columns(area);

    for (column, weekday) in columns.iter().zip(WEEKDAYS) {
        let widget = Paragraph::new(weekday)
            .style(
                Style::default()
                    .add_modifier(Modifier::BOLD),
            );

        frame.render_widget(widget, *column);
    }
}

fn render_month(frame: &mut Frame, app: &App, area: Rect) {
    let weeks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([Constraint::Ratio(1, 6); 6])
        .split(area);

    let first = app.first_day_of_month();

    let offset =
        first.weekday().num_days_from_monday() as u64;

    let grid_start = first - Days::new(offset);

    let today = Local::now().date_naive();

    for week in 0..6 {
        let columns = seven_columns(weeks[week]);

        for (day, column) in columns.iter().enumerate() {
            let index = (week * 7 + day) as u64;
            let date = grid_start + Days::new(index);

            render_day(
                frame,
                *column,
                date,
                app.selected,
                today,
                app.selected.month(),
            );
        }
    }
}

fn render_day(
    frame: &mut Frame,
    area: Rect,
    date: NaiveDate,
    selected: NaiveDate,
    today: NaiveDate,
    visible_month: u32,
) {
    let mut style = Style::default();

    if date.month() != visible_month {
        style = style.add_modifier(Modifier::DIM);
    }

    if date == today {
        style = style.add_modifier(Modifier::UNDERLINED);
    }

    if date == selected {
        style = style.add_modifier(Modifier::REVERSED);
    }

    // Fake data for now.
    let activity = match date.day() % 7 {
        0 => "🥋 Kyokushin",
        2 => "🏃 Run",
        5 => "🏋 Squat",
        _ => "",
    };

    let content = vec![
        Line::from(Span::styled(
            date.day().to_string(),
            Style::default().add_modifier(Modifier::BOLD),
        )),
        Line::from(activity),
    ];

    let widget = Paragraph::new(content)
        .style(style)
        .block(Block::default().borders(Borders::ALL));

    frame.render_widget(widget, area);
}

fn render_help(frame: &mut Frame, area: Rect) {
    frame.render_widget(
        Paragraph::new(
            "h/l day  j/k week  H/L month  t today  q quit",
        ),
        area,
    );
}

fn seven_columns(area: Rect) -> std::rc::Rc<[Rect]> {
    Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Ratio(1, 7); 7])
        .split(area)
}