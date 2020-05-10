"""Schedules spreadsheet table"""

from mysqldb_wrapper import Base, Id
from common.api.spreadsheet import (
    Cell,
    find_corresponding_cell_best_effort,
    find_corresponding_cells_best_effort,
)


class SchedulesSpreadsheet(Base):
    """Schedules spreadsheet class"""

    __tablename__ = "schedules_spreadsheet"

    id = Id()
    spreadsheet_id = str()
    sheet_name = str("")
    range_match_id = str("A2:A")
    range_team1 = str("B2:B")
    range_score_team1 = str("C2:C")
    range_score_team2 = str("D2:D")
    range_team2 = str("E2:E")
    range_date = str("F2:F")
    range_time = str("G2:G")
    range_referee = str("H2:H")
    range_streamer = str("I2:I")
    range_commentator = str("J2:K")
    range_mp_links = str("L2:L")
    date_format = str()
    use_range = bool(False)
    max_referee = int(1)
    max_streamer = int(1)
    max_commentator = int(2)


class MatchIdNotFound(Exception):
    """Thrown when a match id is not found."""

    def __init__(self, match_id):
        self.match_id = match_id


class DuplicateMatchId(Exception):
    """Thrown when a match id is found multiple times."""

    def __init__(self, match_id):
        self.match_id = match_id


class MatchInfo:
    """Contains all info about a match."""

    def __init__(self, match_id_cell):
        self.match_id = match_id_cell
        self.team1 = Cell(-1, -1, "")
        self.team2 = Cell(-1, -1, "")
        self.score_team1 = Cell(-1, -1, "")
        self.score_team2 = Cell(-1, -1, "")
        self.date = Cell(-1, -1, "")
        self.time = Cell(-1, -1, "")
        self.referees = []
        self.streamers = []
        self.commentators = []
        self.mp_links = []

    def get_datetime(self):
        return " ".join(filter(None, [self.date.value, self.time.value]))

    @staticmethod
    def from_id(schedules_spreadsheet, worksheet, match_id, filled_only=True):
        match_id_cells = worksheet.get_range(schedules_spreadsheet.range_match_id)
        corresponding_match_id_cells = worksheet.find_cells(match_id_cells, match_id)
        if not corresponding_match_id_cells:
            raise MatchIdNotFound(match_id)
        if len(corresponding_match_id_cells) > 1:
            raise DuplicateMatchId(match_id)
        match_id_cell = corresponding_match_id_cells[0]
        return MatchInfo.from_match_id_cell(schedules_spreadsheet, worksheet, match_id_cell, filled_only)

    @staticmethod
    def from_match_id_cell(schedules_spreadsheet, worksheet, match_id_cell, filled_only=True):
        match_id_best_effort_ys = match_id_cell.y_merge_range
        match_info = MatchInfo(match_id_cell)
        match_info.team1 = find_corresponding_cell_best_effort(
            worksheet.get_range(schedules_spreadsheet.range_team1), match_id_best_effort_ys, match_id_cell.y,
        )
        match_info.team2 = find_corresponding_cell_best_effort(
            worksheet.get_range(schedules_spreadsheet.range_team2), match_id_best_effort_ys, match_id_cell.y,
        )
        match_info.score_team1 = find_corresponding_cell_best_effort(
            worksheet.get_range(schedules_spreadsheet.range_score_team1), match_id_best_effort_ys, match_id_cell.y,
        )
        match_info.score_team2 = find_corresponding_cell_best_effort(
            worksheet.get_range(schedules_spreadsheet.range_score_team2), match_id_best_effort_ys, match_id_cell.y,
        )
        match_info.date = find_corresponding_cell_best_effort(
            worksheet.get_range(schedules_spreadsheet.range_date), match_id_best_effort_ys, match_id_cell.y,
        )
        match_info.time = find_corresponding_cell_best_effort(
            worksheet.get_range(schedules_spreadsheet.range_time), match_id_best_effort_ys, match_id_cell.y,
        )
        if schedules_spreadsheet.use_range:
            match_info.referees = find_corresponding_cells_best_effort(
                worksheet.get_range(schedules_spreadsheet.range_referee),
                match_id_best_effort_ys,
                match_id_cell.y,
                filled_only,
            )
            match_info.streamers = find_corresponding_cells_best_effort(
                worksheet.get_range(schedules_spreadsheet.range_streamer),
                match_id_best_effort_ys,
                match_id_cell.y,
                filled_only,
            )
            match_info.commentators = find_corresponding_cells_best_effort(
                worksheet.get_range(schedules_spreadsheet.range_commentator),
                match_id_best_effort_ys,
                match_id_cell.y,
                filled_only,
            )
            match_info.mp_links = find_corresponding_cells_best_effort(
                worksheet.get_range(schedules_spreadsheet.range_mp_links),
                match_id_best_effort_ys,
                match_id_cell.y,
                filled_only,
            )
        else:
            match_info.referees = [
                find_corresponding_cell_best_effort(
                    worksheet.get_range(schedules_spreadsheet.range_referee), match_id_best_effort_ys, match_id_cell.y,
                )
            ]
            match_info.streamers = [
                find_corresponding_cell_best_effort(
                    worksheet.get_range(schedules_spreadsheet.range_streamer), match_id_best_effort_ys, match_id_cell.y,
                )
            ]
            match_info.commentators = [
                find_corresponding_cell_best_effort(
                    worksheet.get_range(schedules_spreadsheet.range_commentator),
                    match_id_best_effort_ys,
                    match_id_cell.y,
                )
            ]
            match_info.mp_links = [
                find_corresponding_cell_best_effort(
                    worksheet.get_range(schedules_spreadsheet.range_mp_links), match_id_best_effort_ys, match_id_cell.y,
                )
            ]
        return match_info
