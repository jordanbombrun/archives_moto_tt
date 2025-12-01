from RankingMotoApp.app.dao.participation_dao import dao_get_participations_by_race
from RankingMotoApp.app.utils import DBReport


class RiderService:
    def get_participations_by_race(self, race_id: int):
        try:
            result = dao_get_participations_by_race(race_id)
            return result
        except Exception:
            return DBReport.GET_ERROR

    # def get_participation_(self, participation_id: int):
        # 
