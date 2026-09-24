use chrono::{Datelike, Days, Local, Months, NaiveDate};

pub struct App {
    pub selected: NaiveDate,
}

impl App {
    pub fn new() -> Self {
        Self {
            selected: Local::now().date_naive(),
        }
    }

    pub fn today(&mut self) {
        self.selected = Local::now().date_naive();
    }

    pub fn previous_day(&mut self) {
        self.selected = self.selected - Days::new(1);
    }

    pub fn next_day(&mut self) {
        self.selected = self.selected + Days::new(1);
    }

    pub fn previous_week(&mut self) {
        self.selected = self.selected - Days::new(7);
    }

    pub fn next_week(&mut self) {
        self.selected = self.selected + Days::new(7);
    }

    pub fn previous_month(&mut self) {
        if let Some(date) = self.selected.checked_sub_months(Months::new(1)) {
            self.selected = date;
        }
    }

    pub fn next_month(&mut self) {
        if let Some(date) = self.selected.checked_add_months(Months::new(1)) {
            self.selected = date;
        }
    }

    pub fn first_day_of_month(&self) -> NaiveDate {
        self.selected.with_day(1).unwrap()
    }
}