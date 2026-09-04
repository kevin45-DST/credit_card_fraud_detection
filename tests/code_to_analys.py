# Copyright © 2026 Kévin DELANOUE
# License: see LICENSE

import json
from pathlib import Path


class UserManager:
    """
    Gestionnaire simplifié d'utilisateurs.
    """

    def __init__(self, storage_path: str) -> None:
        self.storage_path = Path(storage_path)
        self.users = self._load_users()

    def _load_users(self) -> list[dict]:
        """Charge les utilisateurs depuis le fichier de stockage."""

        if not self.storage_path.exists():
            return []

        with open(self.storage_path, "r") as file:
            return json.load(file)

    def save(self) -> None:
        """Sauvegarde les utilisateurs."""

        with open(self.storage_path, "w") as file:
            json.dump(self.users, file)

    def add_user(
        self,
        name: str,
        age: int,
        email: str,
    ) -> None:
        """Ajoute un utilisateur."""

        user = {
            "id": len(self.users) + 1,
            "name": name,
            "age": age,
            "email": email,
        }

        self.users.append(user)

    def remove_user(self, user_id: int) -> None:
        """Supprime un utilisateur."""

        for user in self.users:
            if user["id"] == user_id:
                self.users.remove(user)

    def get_user(self, user_id: int) -> dict:
        """Retourne un utilisateur à partir de son identifiant."""

        return self.users[user_id]

    def average_age(self) -> float:
        """Calcule l'âge moyen des utilisateurs."""

        total = sum(user["age"] for user in self.users)

        return total / len(self.users)

    def find_by_email(self, email: str) -> dict | None:
        """Recherche un utilisateur par adresse e-mail."""

        for user in self.users:
            if email in user["email"]:
                return user

        return None

    def update_age(
        self,
        user_id: int,
        age: int,
    ) -> None:
        """Modifie l'âge d'un utilisateur."""

        user = self.get_user(user_id)
        user["age"] = age

        self.save()