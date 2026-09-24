mod app;
mod ui;

use std::{
    io,
    time::Duration,
};

use crossterm::event::{self, Event, KeyCode};
use ratatui::{
    Terminal,
    backend::CrosstermBackend,
    crossterm::{
        execute,
        terminal::{
            EnterAlternateScreen,
            LeaveAlternateScreen,
            disable_raw_mode,
            enable_raw_mode,
        },
    },
};

use crate::app::App;

fn main() -> io::Result<()> {
    enable_raw_mode()?;

    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;

    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    let result = run(&mut terminal);

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
    terminal.show_cursor()?;

    result
}

fn run(
    terminal: &mut Terminal<CrosstermBackend<io::Stdout>>,
) -> io::Result<()> {
    let mut app = App::new();

    loop {
        terminal.draw(|frame| ui::render(frame, &app))?;

        if !event::poll(Duration::from_millis(250))? {
            continue;
        }

        let Event::Key(key) = event::read()? else {
            continue;
        };

        match key.code {
            KeyCode::Char('q') => return Ok(()),

            KeyCode::Char('h') => app.previous_day(),
            KeyCode::Char('l') => app.next_day(),

            KeyCode::Char('k') => app.previous_week(),
            KeyCode::Char('j') => app.next_week(),

            KeyCode::Char('H') => app.previous_month(),
            KeyCode::Char('L') => app.next_month(),

            KeyCode::Char('t') => app.today(),

            _ => {}
        }
    }
}