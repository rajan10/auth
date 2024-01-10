from auth.model import User


class UserRepo:
    def create(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        user.save()
        return user

    def read_by_username(self, username: str) -> User:
        user = User.objects.get(
            username=username
        )  # from a model class representing users, get/fetch as single user object
        if user:
            return user

    def read_all(self) -> list[User]:
        users = User.objects()
        if users:
            return list(users)
        return []

    def update_by_username(self, username: str, password: str) -> User:
        user = User.Objects.get(username=username)
        if user:
            user.password = password
            user.save()
        return user

    def delete_by_username(self, username: str) -> None:
        user = User.Objects.get(username=username)
        if user:
            user.delete()
