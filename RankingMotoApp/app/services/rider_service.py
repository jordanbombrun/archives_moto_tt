from RankingMotoApp.app.dao.participation_dao import (
    dao_get_participations_by_race,
    dao_get_participation_by_race_rider,
)
from RankingMotoApp.app.models.race import Race
from RankingMotoApp.app.models.rider import Rider
from RankingMotoApp.app.utils.DBReport import DBReport


class RiderService:
    def get_participations_by_race(self, race_id: int):
        try:
            result = dao_get_participations_by_race(race_id)
            return result
        except Exception:
            return DBReport.GET_ERROR

    def get_participation_by_race_and_rider(self, race: Race, rider_id: int):
        try:
            rider = Rider(db_id=rider_id)
            result = dao_get_participation_by_race_rider(race, rider)
            return result
        except Exception:
            return DBReport.GET_ERROR


