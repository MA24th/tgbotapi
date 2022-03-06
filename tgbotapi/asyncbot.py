from .bot import Bot
from .utils import async_dec

""" This is AsyncBot module """


class AsyncBot(Bot):
    def __init__(self, *args, **kwargs):
        Bot.__init__(self, *args, **kwargs)

    @async_dec()
    def set_webhook(self, *args, **kwargs):
        return Bot.set_webhook(self, *args, **kwargs)

    @async_dec()
    def delete_webhook(self, *args, **kwargs):
        return Bot.delete_webhook(self, *args, **kwargs)

    @async_dec()
    def get_webhook_info(self):
        return Bot.get_webhook_info(self)

    @async_dec()
    def get_me(self):
        return Bot.get_me(self)

    @async_dec()
    def log_out(self):
        return Bot.log_out(self)

    @async_dec()
    def close(self):
        return Bot.close(self)

    @async_dec()
    def send_message(self, *args, **kwargs):
        return Bot.send_message(self, *args, **kwargs)

    @async_dec()
    def forward_message(self, *args, **kwargs):
        return Bot.forward_message(self, *args, **kwargs)

    @async_dec()
    def copy_message(self, *args, **kwargs):
        return Bot.copy_message(self, *args, **kwargs)

    @async_dec()
    def send_photo(self, *args, **kwargs):
        return Bot.send_photo(self, *args, **kwargs)

    @async_dec()
    def send_audio(self, *args, **kwargs):
        return Bot.send_audio(self, *args, **kwargs)

    @async_dec()
    def send_document(self, *args, **kwargs):
        return Bot.send_document(self, *args, **kwargs)

    @async_dec()
    def send_video(self, *args, **kwargs):
        return Bot.send_video(self, *args, **kwargs)

    @async_dec()
    def sen_animation(self, *args, **kwargs):
        return Bot.send_animation(self, *args, **kwargs)

    @async_dec()
    def send_voice(self, *args, **kwargs):
        return Bot.send_voice(self, *args, **kwargs)

    @async_dec()
    def send_video_note(self, *args, **kwargs):
        return Bot.send_video_note(self, *args, **kwargs)

    @async_dec()
    def send_media_group(self, *args, **kwargs):
        return Bot.send_media_group(self, *args, **kwargs)

    @async_dec()
    def send_location(self, *args, **kwargs):
        return Bot.send_location(self, *args, **kwargs)

    @async_dec()
    def edit_message_live_location(self, *args, **kwargs):
        return Bot.edit_message_live_location(self, *args, **kwargs)

    @async_dec()
    def stop_message_live_location(self, *args, **kwargs):
        return Bot.stop_message_live_location(self, *args, **kwargs)

    @async_dec()
    def send_venue(self, *args, **kwargs):
        return Bot.send_venue(self, *args, **kwargs)

    @async_dec()
    def send_contact(self, *args, **kwargs):
        return Bot.send_contact(self, *args, **kwargs)

    @async_dec()
    def send_poll(self, *args, **kwargs):
        return Bot.send_poll(self, *args, **kwargs)

    @async_dec()
    def send_dice(self, *args, **kwargs):
        return Bot.send_dice(self, *args, **kwargs)

    @async_dec()
    def send_chat_action(self, *args, **kwargs):
        return Bot.send_chat_action(self, *args, **kwargs)

    @async_dec()
    def get_user_profile_photos(self, *args, **kwargs):
        return Bot.get_user_profile_photos(self, *args, **kwargs)

    @async_dec()
    def get_file(self, *args):
        return Bot.get_file(self, *args)

    @async_dec()
    def kick_chat_member(self, *args, **kwargs):
        return Bot.kick_chat_member(self, *args, **kwargs)

    @async_dec()
    def unban_chat_member(self, *args):
        return Bot.unban_chat_member(self, *args)

    @async_dec()
    def restrict_chat_member(self, *args, **kwargs):
        return Bot.restrict_chat_member(self, *args, **kwargs)

    @async_dec()
    def promote_chat_member(self, *args, **kwargs):
        return Bot.promote_chat_member(self, *args, **kwargs)

    @async_dec()
    def set_chat_administrator_custom_title(self, *args, **kwargs):
        return Bot.set_chat_administrator_custom_title(self, *args, **kwargs)

    @async_dec()
    def set_chat_permissions(self, *args, **kwargs):
        return Bot.set_chat_permissions(self, *args, **kwargs)

    @async_dec()
    def export_chat_invite_link(self, *args):
        return Bot.export_chat_invite_link(self, *args)

    @async_dec()
    def create_chat_invite_link(self, *args, **kwargs):
        return Bot.create_chat_invite_link(self, *args, **kwargs)

    @async_dec()
    def edit_chat_invite_link(self, *args, **kwargs):
        return Bot.edit_chat_invite_link(self, *args, **kwargs)

    @async_dec()
    def revoke_chat_invite_link(self, *args, **kwargs):
        return Bot.revoke_chat_invite_link(self, *args, **kwargs)

    @async_dec()
    def set_chat_photo(self, *args):
        return Bot.set_chat_photo(self, *args)

    @async_dec()
    def delete_chat_photo(self, *args):
        return Bot.delete_chat_photo(self, *args)

    @async_dec()
    def set_chat_title(self, *args):
        return Bot.set_chat_title(self, *args)

    @async_dec()
    def set_chat_description(self, *args):
        return Bot.set_chat_description(self, *args)

    @async_dec()
    def pin_chat_message(self, *args, **kwargs):
        return Bot.pin_chat_message(self, *args, **kwargs)

    @async_dec()
    def unpin_chat_message(self, *args):
        return Bot.unpin_chat_message(self, *args)

    @async_dec()
    def unpin_all_chat_message(self, *args):
        return Bot.unpin_all_chat_message(self, *args)

    @async_dec()
    def leave_chat(self, *args):
        return Bot.leave_chat(self, *args)

    @async_dec()
    def get_chat(self, *args):
        return Bot.get_chat(self, *args)

    @async_dec()
    def get_chat_administrators(self, *args):
        return Bot.get_chat_administrators(self, *args)

    @async_dec()
    def get_chat_members_count(self, *args):
        return Bot.get_chat_members_count(self, *args)

    @async_dec()
    def get_chat_member(self, *args):
        return Bot.get_chat_member(self, *args)

    @async_dec()
    def set_chat_sticker_set(self, *args):
        return Bot.set_chat_sticker_set(self, *args)

    @async_dec()
    def delete_chat_sticker_set(self, *args):
        return Bot.delete_chat_sticker_set(self, *args)

    @async_dec()
    def answer_callback_query(self, *args, **kwargs):
        return Bot.answer_callback_query(self, *args, **kwargs)

    @async_dec()
    def set_my_commands(self, *args):
        return Bot.set_my_commands(self, *args)

    @async_dec()
    def get_my_commands(self):
        return Bot.get_my_commands(self)

    @async_dec()
    def edit_message_text(self, *args, **kwargs):
        return Bot.edit_message_text(self, *args, **kwargs)

    @async_dec()
    def edit_message_caption(self, *args, **kwargs):
        return Bot.edit_message_caption(self, *args, **kwargs)

    @async_dec()
    def edit_message_media(self, *args, **kwargs):
        return Bot.edit_message_media(self, *args, **kwargs)

    @async_dec()
    def edit_message_reply_markup(self, *args, **kwargs):
        return Bot.edit_message_reply_markup(self, *args, **kwargs)

    @async_dec()
    def stop_poll(self, *args, **kwargs):
        return Bot.stop_poll(self, *args, **kwargs)

    @async_dec()
    def delete_message(self, *args):
        return Bot.delete_message(self, *args)

    @async_dec()
    def send_sticker(self, *args, **kwargs):
        return Bot.send_sticker(self, *args, **kwargs)

    @async_dec()
    def get_sticker_set(self, *args, **kwargs):
        return Bot.get_sticker_set(self, *args, **kwargs)

    @async_dec()
    def upload_sticker_file(self, *args, **kwargs):
        return Bot.upload_sticker_file(self, *args, **kwargs)

    @async_dec()
    def create_new_sticker_set(self, *args, **kwargs):
        return Bot.create_new_sticker_set(self, *args, **kwargs)

    @async_dec()
    def add_sticker_to_set(self, *args, **kwargs):
        return Bot.add_sticker_to_set(self, *args, **kwargs)

    @async_dec()
    def set_sticker_position_in_set(self, *args, **kwargs):
        return Bot.set_sticker_position_in_set(self, *args, **kwargs)

    @async_dec()
    def delete_sticker_from_set(self, *args, **kwargs):
        return Bot.delete_sticker_from_set(self, *args, **kwargs)

    @async_dec()
    def set_sticker_set_thumb(self, *args, **kwargs):
        return Bot.set_sticker_set_thumb(self, *args, **kwargs)

    @async_dec()
    def answer_inline_query(self, *args, **kwargs):
        return Bot.answer_inline_query(self, *args, **kwargs)

    @async_dec()
    def send_invoice(self, *args, **kwargs):
        return Bot.send_invoice(self, *args, **kwargs)

    @async_dec()
    def answer_shipping_query(self, *args, **kwargs):
        return Bot.answer_shipping_query(self, *args, **kwargs)

    @async_dec()
    def answer_pre_checkout_query(self, *args, **kwargs):
        return Bot.answer_pre_checkout_query(self, *args, **kwargs)

    @async_dec()
    def set_passport_data_errors(self, *args, **kwargs):
        return Bot.set_passport_data_errors(self, *args, **kwargs)

    @async_dec()
    def send_game(self, *args, **kwargs):
        return Bot.send_game(self, *args, **kwargs)

    @async_dec()
    def set_game_score(self, *args, **kwargs):
        return Bot.set_game_score(self, *args, **kwargs)

    @async_dec()
    def get_game_high_scores(self, *args, **kwargs):
        return Bot.get_game_high_scores(self, *args, **kwargs)
