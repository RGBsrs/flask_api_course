from src.database.models import Actor


class ActorService:
    @staticmethod
    def fetch_all_actors(session):
        return session.query(Actor)

    @classmethod
    def fetch_actor_by_name(cls, session, name):
        return cls.fetch_all_actors(session).filter_by(name = name).first()
