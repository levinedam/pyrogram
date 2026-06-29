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

import pyrogram
from pyrogram import enums, raw, types

from ..object import Object


class InlineKeyboardButton(Object):
    """One button of an inline keyboard.

    You must use exactly one of the optional fields.

    Parameters:
        text (``str``):
            Label text on the button.

        callback_data (``str`` | ``bytes``, *optional*):
            Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes.

        url (``str``, *optional*):
            HTTP url to be opened when button is pressed.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            Description of the `Web App <https://core.telegram.org/bots/webapps>`_ that will be launched when the user
            presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the
            method :meth:`~pyrogram.Client.answer_web_app_query`. Available only in private chats between a user and the
            bot.

        login_url (:obj:`~pyrogram.types.LoginUrl`, *optional*):
             An HTTP URL used to automatically authorize the user. Can be used as a replacement for
             the `Telegram Login Widget <https://core.telegram.org/widgets/login>`_.

        user_id (``int``, *optional*):
            User id, for links to the user profile.

        switch_inline_query (``str``, *optional*):
            If set, pressing the button will prompt the user to select one of their chats, open that chat and insert
            the bot's username and the specified inline query in the input field. Can be empty, in which case just
            the bot's username will be inserted.

        switch_inline_query_current_chat (``str``, *optional*):
            If set, pressing the button will insert the bot's username and the specified inline query in the current
            chat's input field. Can be empty, in which case only the bot's username will be inserted.

        callback_game (:obj:`~pyrogram.types.CallbackGame`, *optional*):
            Description of the game that will be launched when the user presses the button.
            **NOTE**: This type of button **must** always be the first button in the first row.

        requires_password (``bool``, *optional*):
            A button that asks for 2-step verification password before sending callback query.

        pay (``bool``, *optional*):
            Pass True, to send a Pay button.

        copy_text (``str``, *optional*):
            A button that copies specified text to clipboard.
            Limited to 256 character.

        icon_custom_emoji_id (``str``, *optional*):
            Identifier of the custom emoji that must be shown on the button.

        style (:obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Style of the button.
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
            return None

        if style == enums.ButtonStyle.DEFAULT and icon_custom_emoji_id is None:
            return None

        return kbs(
            bg_primary=style == enums.ButtonStyle.PRIMARY,
            bg_danger=style == enums.ButtonStyle.DANGER,
            bg_success=style == enums.ButtonStyle.SUCCESS,
            icon=int(icon_custom_emoji_id) if icon_custom_emoji_id is not None else None
        )

    @staticmethod
    def _construct_raw(cls, **kwargs):
        try:
            return cls(**kwargs)
        except TypeError:
            kwargs.pop("style", None)
            return cls(**kwargs)

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