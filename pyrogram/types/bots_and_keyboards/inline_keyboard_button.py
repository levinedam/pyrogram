#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, Union
import logging

import pyrogram
from pyrogram import enums, raw, types

from ..object import Object

log = logging.getLogger("pyrogram.button_style_debug")


class InlineKeyboardButton(Object):
    """One button of an inline keyboard.

    You must use exactly one of the optional fields.
    """

    def __init__(
        self,
        text: str,
        callback_data: Optional[Union[str, bytes]] = None,
        url: Optional[str] = None,
        web_app: Optional["types.WebAppInfo"] = None,
        login_url: Optional["types.LoginUrl"] = None,
        user_id: Optional[int] = None,
        switch_inline_query: Optional[str] = None,
        switch_inline_query_current_chat: Optional[str] = None,
        callback_game: Optional["types.CallbackGame"] = None,
        requires_password: Optional[bool] = None,
        pay: Optional[bool] = None,
        copy_text: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None,
        style: "enums.ButtonStyle" = enums.ButtonStyle.DEFAULT
    ):
        super().__init__()

        self.text = str(text)
        self.callback_data = callback_data
        self.url = url
        self.web_app = web_app
        self.login_url = login_url
        self.user_id = user_id
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.requires_password = requires_password
        self.pay = pay
        self.copy_text = copy_text
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    @staticmethod
    def _build_raw_button_style(style, icon_custom_emoji_id):
        kbs = getattr(raw.types, "KeyboardButtonStyle", None)
        if kbs is None:
            log.warning("[IKB._build_raw_button_style] KeyboardButtonStyle not found in raw.types")
            return None

        if style == enums.ButtonStyle.DEFAULT and icon_custom_emoji_id is None:
            return None

        try:
            obj = kbs(
                bg_primary=style == enums.ButtonStyle.PRIMARY,
                bg_danger=style == enums.ButtonStyle.DANGER,
                bg_success=style == enums.ButtonStyle.SUCCESS,
                icon=int(icon_custom_emoji_id) if icon_custom_emoji_id is not None else None
            )
            return obj
        except Exception as e:
            log.warning("[IKB._build_raw_button_style] failed to build style: %r", e)
            return None

    @staticmethod
    def _construct_raw(cls, **kwargs):
        try:
            obj = cls(**kwargs)
            log.warning("[IKB._construct_raw] OK cls=%s has_style=%s", cls.__name__, "style" in kwargs)
            return obj
        except TypeError as e:
            had_style = "style" in kwargs
            log.warning(
                "[IKB._construct_raw] TypeError cls=%s had_style=%s err=%s -> retry without style",
                cls.__name__, had_style, e
            )
            kwargs.pop("style", None)
            obj = cls(**kwargs)
            log.warning("[IKB._construct_raw] RETRY OK cls=%s", cls.__name__)
            return obj

    @staticmethod
    def read(b: "raw.base.KeyboardButton"):
        raw_style = getattr(b, "style", None)
        button_style = enums.ButtonStyle.DEFAULT
        icon_custom_emoji_id = None

        if raw_style is not None:
            if getattr(raw_style, "bg_primary", False):
                button_style = enums.ButtonStyle.PRIMARY
            elif getattr(raw_style, "bg_danger", False):
                button_style = enums.ButtonStyle.DANGER
            elif getattr(raw_style, "bg_success", False):
                button_style = enums.ButtonStyle.SUCCESS

            raw_icon = getattr(raw_style, "icon", None)
            if raw_icon:
                icon_custom_emoji_id = str(raw_icon)

        if isinstance(b, raw.types.KeyboardButtonCallback):
            try:
                data = b.data.decode()
            except UnicodeDecodeError:
                data = b.data

            return InlineKeyboardButton(
                text=b.text,
                callback_data=data,
                requires_password=getattr(b, "requires_password", None),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonUrl):
            return InlineKeyboardButton(
                text=b.text,
                url=b.url,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonUrlAuth):
            return InlineKeyboardButton(
                text=b.text,
                login_url=types.LoginUrl.read(b),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonUserProfile):
            return InlineKeyboardButton(
                text=b.text,
                user_id=b.user_id,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonSwitchInline):
            if b.same_peer:
                return InlineKeyboardButton(
                    text=b.text,
                    switch_inline_query_current_chat=b.query,
                    style=button_style,
                    icon_custom_emoji_id=icon_custom_emoji_id
                )
            else:
                return InlineKeyboardButton(
                    text=b.text,
                    switch_inline_query=b.query,
                    style=button_style,
                    icon_custom_emoji_id=icon_custom_emoji_id
                )

        if isinstance(b, raw.types.KeyboardButtonGame):
            return InlineKeyboardButton(
                text=b.text,
                callback_game=types.CallbackGame(),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonWebView):
            return InlineKeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(url=b.url),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonBuy):
            return InlineKeyboardButton(
                text=b.text,
                pay=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonCopy):
            return InlineKeyboardButton(
                text=b.text,
                copy_text=b.copy_text,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButton):
            return InlineKeyboardButton(
                text=b.text,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

    async def write(self, client: "pyrogram.Client"):
        style = self._build_raw_button_style(self.style, self.icon_custom_emoji_id)

        log.warning(
            "[IKB.write] text=%r style=%r icon=%r raw_style=%r",
            self.text, self.style, self.icon_custom_emoji_id, style
        )

        if self.callback_data is not None:
            data = bytes(self.callback_data, "utf-8") if isinstance(self.callback_data, str) else self.callback_data
            return self._construct_raw(
                raw.types.KeyboardButtonCallback,
                text=self.text,
                data=data,
                requires_password=self.requires_password,
                style=style
            )

        if self.url is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonUrl,
                text=self.text,
                url=self.url,
                style=style
            )

        if self.login_url is not None:
            try:
                return self.login_url.write(
                    text=self.text,
                    bot=await client.resolve_peer(self.login_url.bot_username or "self"),
                    style=style
                )
            except TypeError:
                log.warning("[IKB.write] login_url.write does not support style, retry without style")
                return self.login_url.write(
                    text=self.text,
                    bot=await client.resolve_peer(self.login_url.bot_username or "self")
                )

        if self.user_id is not None:
            return self._construct_raw(
                raw.types.InputKeyboardButtonUserProfile,
                text=self.text,
                user_id=await client.resolve_peer(self.user_id),
                style=style
            )

        if self.switch_inline_query is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonSwitchInline,
                text=self.text,
                query=self.switch_inline_query,
                style=style
            )

        if self.switch_inline_query_current_chat is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonSwitchInline,
                text=self.text,
                query=self.switch_inline_query_current_chat,
                same_peer=True,
                style=style
            )

        if self.callback_game is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonGame,
                text=self.text,
                style=style
            )

        if self.web_app is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonWebView,
                text=self.text,
                url=self.web_app.url,
                style=style
            )

        if self.pay is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonBuy,
                text=self.text,
                style=style
            )

        if self.copy_text is not None:
            return self._construct_raw(
                raw.types.KeyboardButtonCopy,
                text=self.text,
                copy_text=self.copy_text,
                style=style
            )