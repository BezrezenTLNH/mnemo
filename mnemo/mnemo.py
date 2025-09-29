"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import httpx
import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    email: str = ""
    password: str = ""
    registration_message: str = ""

    async def register_user(self, form_data):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "http://localhost:8000/register",
                json={"email": form_data["email"], "password": form_data["password"]},
            )
            try:
                data = resp.json()
            except Exception:
                self.registration_message = f"Ошибка: {resp.text}"
                return
            if resp.status_code == 200:
                self.registration_message = "Успешно зарегистрирован!"
            else:
                self.registration_message = (
                    f"Ошибка: {data.get('detail', 'Неизвестная ошибка')}"
                )


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Mneno!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(rx.button("Register Now", color_scheme="teal"), href="/register"),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


def register_page() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Registration", size="7"),
            rx.form(
                rx.input(placeholder="Email", name="email"),
                rx.input(placeholder="Password", name="password", type_="password"),
                rx.button("Register", type_="submit"),
                on_submit=State.register_user,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(register_page, route="/register")
