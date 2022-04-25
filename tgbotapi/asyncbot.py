# -*- coding: utf-8 -*-

"""
tgbotapi.asyncbot
~~~~~~~~~~~~~~~~~
This submodule provides an AsyncBot object to manage and persist settings across
tgbotapi (based_url, allowed_update, threaded, skip_pending, num_threads, proxies).
"""

from .bot import Bot
from .utils import async_dec


class AsyncBot(Bot):
    def __init__(self, access_token, threaded=True, num_threads=12, based_url=None, proxies=None):
        Bot.__init__(self, access_token, threaded, num_threads, based_url, proxies)

    @async_dec()
    def set_webhook(self, url, certificate=None, ip_address=None, max_connections=40, allowed_updates=None,
                    drop_pending_updates=False):
        return Bot.set_webhook(self, url, certificate, ip_address, max_connections, allowed_updates,
                               drop_pending_updates)

    @async_dec()
    def delete_webhook(self, drop_pending_updates=False):
        return Bot.delete_webhook(self, drop_pending_updates)

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
    def send_message(self, chat_id, text, parse_mode=None, entities=None, disable_web_page_preview=False,
                     disable_notification=False, protect_content=False, reply_to_message_id=None,
                     allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_message(self, chat_id, text, parse_mode, entities, disable_web_page_preview,
                                disable_notification, protect_content, reply_to_message_id, allow_sending_without_reply,
                                reply_markup)

    @async_dec()
    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=False, protect_content=False):
        return Bot.forward_message(self, chat_id, from_chat_id, message_id, disable_notification, protect_content)

    @async_dec()
    def copy_message(self, chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None,
                     disable_notification=False, protect_content=False, reply_to_message_id=None,
                     allow_sending_without_reply=False, reply_markup=None):
        return Bot.copy_message(self, chat_id, from_chat_id, message_id, caption, parse_mode, caption_entities,
                                disable_notification, protect_content, reply_to_message_id, allow_sending_without_reply,
                                reply_markup)

    @async_dec()
    def send_photo(self, chat_id, photo, caption=None, parse_mode=None, caption_entities=None,
                   disable_notification=False, protect_content=False, reply_to_message_id=None,
                   allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_photo(self, chat_id, photo, caption, parse_mode, caption_entities, disable_notification,
                              protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_audio(self, chat_id, audio, caption=None, parse_mode=None, caption_entities=None, duration=None,
                   performer=None, title=None, thumb=None, disable_notification=False, protect_content=False,
                   reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_audio(self, chat_id, audio, caption, parse_mode, caption_entities, duration, performer, title,
                              thumb, disable_notification, protect_content, reply_to_message_id,
                              allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_document(self, chat_id, document, thumb=None, caption=None, parse_mode=None, caption_entities=None,
                      disable_content_type_detection=False, disable_notification=False, protect_content=False,
                      reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_document(self, chat_id, document, thumb, caption, parse_mode, caption_entities,
                                 disable_content_type_detection, disable_notification, protect_content,
                                 reply_to_message_id, allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_video(self, chat_id, video, duration=None, width=None, height=None, thumb=None, caption=None,
                   parse_mode=None, caption_entities=None, supports_streaming=None, disable_notification=False,
                   protect_content=False, reply_to_message_id=None, allow_sending_without_reply=False,
                   reply_markup=None):
        return Bot.send_video(self, chat_id, video, duration, width, height, thumb, caption, parse_mode,
                              caption_entities, supports_streaming, disable_notification, protect_content,
                              reply_to_message_id, allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_animation(self, chat_id, animation, duration=None, width=None, height=None, thumb=None, caption=None,
                       parse_mode=None, caption_entities=None, disable_notification=False, protect_content=False,
                       reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_animation(self, chat_id, animation, duration, width, height, thumb, caption, parse_mode,
                                  caption_entities, disable_notification, protect_content, reply_to_message_id,
                                  allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_voice(self, chat_id, voice, caption=None, parse_mode=None, caption_entities=None, duration=None,
                   disable_notification=False, protect_content=False, reply_to_message_id=None,
                   allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_voice(self, chat_id, voice, caption, parse_mode, caption_entities, duration,
                              disable_notification, protect_content, reply_to_message_id, allow_sending_without_reply,
                              reply_markup)

    @async_dec()
    def send_video_note(self, chat_id, video_note, duration=None, length=None, thumb=None, disable_notification=False,
                        protect_content=False, reply_to_message_id=None, allow_sending_without_reply=False,
                        reply_markup=None):
        return Bot.send_video_note(self, chat_id, video_note, duration, length, thumb, disable_notification,
                                   protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_media_group(self, chat_id, media, disable_notification=False, protect_content=False,
                         reply_to_message_id=None, allow_sending_without_reply=False):
        return Bot.send_media_group(self, chat_id, media, disable_notification, protect_content, reply_to_message_id,
                                    allow_sending_without_reply)

    @async_dec()
    def send_location(self, chat_id, latitude, longitude, horizontal_accuracy=None, live_period=None, heading=None,
                      proximity_alert_radius=None, disable_notification=False, protect_content=False,
                      reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_location(self, chat_id, latitude, longitude, horizontal_accuracy, live_period, heading,
                                 proximity_alert_radius, disable_notification, protect_content, reply_to_message_id,
                                 allow_sending_without_reply, reply_markup)

    @async_dec()
    def edit_message_live_location(self, latitude, longitude, horizontal_accuracy=None, heading=None,
                                   proximity_alert_radius=None, chat_id=None, message_id=None, inline_message_id=None,
                                   reply_markup=None):
        return Bot.edit_message_live_location(self, latitude, longitude, horizontal_accuracy, heading,
                                              proximity_alert_radius, chat_id, message_id, inline_message_id,
                                              reply_markup)

    @async_dec()
    def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return Bot.stop_message_live_location(self, chat_id, message_id, inline_message_id, reply_markup)

    @async_dec()
    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None,
                   google_place_id=None, google_place_type=None, disable_notification=False, protect_content=False,
                   reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id, foursquare_type,
                              google_place_id, google_place_type, disable_notification, protect_content,
                              reply_to_message_id, allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_contact(self, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=False,
                     protect_content=False, reply_to_message_id=None, allow_sending_without_reply=False,
                     reply_markup=None):
        return Bot.send_contact(self, chat_id, phone_number, first_name, last_name, vcard, disable_notification,
                                protect_content, reply_to_message_id, allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_poll(self, chat_id, question, options, is_anonymous=True, ttype='regular', allows_multiple_answers=False,
                  correct_option_id=None, explanation=None, explanation_parse_mode=None, explanation_entities=None,
                  open_period=None, close_date=None, is_closed=True, disable_notifications=False, protect_content=False,
                  reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_poll(self, chat_id, question, options, is_anonymous, ttype, allows_multiple_answers,
                             correct_option_id, explanation, explanation_parse_mode, explanation_entities, open_period,
                             close_date, is_closed, disable_notifications, protect_content, reply_to_message_id,
                             allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_dice(self, chat_id, emoji='🎲', disable_notification=False, protect_content=False,
                  reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_dice(self, chat_id, emoji, disable_notification, protect_content, reply_to_message_id,
                             allow_sending_without_reply, reply_markup)

    @async_dec()
    def send_chat_action(self, chat_id, action):
        return Bot.send_chat_action(self, chat_id, action)

    @async_dec()
    def get_user_profile_photos(self, user_id, offset=None, limit=100):
        return Bot.get_user_profile_photos(self, user_id, offset, limit)

    @async_dec()
    def get_file(self, file_id):
        return Bot.get_file(self, file_id)

    @async_dec()
    def ban_chat_member(self, chat_id, user_id, until_date, revoke_messages):
        return Bot.ban_chat_member(self, chat_id, user_id, until_date, revoke_messages)

    @async_dec()
    def unban_chat_member(self, chat_id, user_id, only_if_banned):
        return Bot.unban_chat_member(self, chat_id, user_id, only_if_banned)

    @async_dec()
    def restrict_chat_member(self, chat_id, user_id, permissions, until_date=None):
        return Bot.restrict_chat_member(self, chat_id, user_id, permissions, until_date)

    @async_dec()
    def promote_chat_member(self, chat_id, user_id, is_anonymous=False, can_manage_chat=False, can_change_info=False,
                            can_post_messages=False, can_edit_messages=False, can_delete_messages=False,
                            can_manage_voice_chats=False, can_invite_users=False, can_restrict_members=False,
                            can_pin_messages=False, can_promote_members=False):
        return Bot.promote_chat_member(self, chat_id, user_id, is_anonymous, can_manage_chat, can_change_info,
                                       can_post_messages, can_edit_messages, can_delete_messages,
                                       can_manage_voice_chats, can_invite_users, can_restrict_members, can_pin_messages,
                                       can_promote_members)

    @async_dec()
    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
        return Bot.set_chat_administrator_custom_title(self, chat_id, user_id, custom_title)

    @async_dec()
    def ban_chat_sender_chat(self, chat_id, sender_chat_id):
        return Bot.ban_chat_sender_chat(self, chat_id, sender_chat_id)

    @async_dec()
    def unban_chat_sender_chat(self, chat_id, sender_chat_id):
        return Bot.unban_chat_sender_chat(self, chat_id, sender_chat_id)

    @async_dec()
    def set_chat_permissions(self, chat_id, permissions):
        return Bot.set_chat_permissions(self, chat_id, permissions)

    @async_dec()
    def export_chat_invite_link(self, chat_id):
        return Bot.export_chat_invite_link(self, chat_id)

    @async_dec()
    def create_chat_invite_link(self, chat_id, name=None, expire_date=None, member_limit=None,
                                creates_join_request=False):
        return Bot.create_chat_invite_link(self, chat_id, name, expire_date, member_limit, creates_join_request)

    @async_dec()
    def edit_chat_invite_link(self, chat_id, invite_link, name=None, expire_date=None, member_limit=None,
                              creates_join_request=False):
        return Bot.edit_chat_invite_link(self, chat_id, invite_link, name, expire_date, member_limit,
                                         creates_join_request)

    @async_dec()
    def revoke_chat_invite_link(self, chat_id, invite_link):
        return Bot.revoke_chat_invite_link(self, chat_id, invite_link)

    @async_dec()
    def approve_chat_join_request(self, chat_id, user_id):
        return Bot.approve_chat_join_request(self, chat_id, user_id)

    @async_dec()
    def decline_chat_join_request(self, chat_id, user_id):
        return Bot.decline_chat_join_request(self, chat_id, user_id)

    @async_dec()
    def set_chat_photo(self, chat_id, photo):
        return Bot.set_chat_photo(self, chat_id, photo)

    @async_dec()
    def delete_chat_photo(self, chat_id):
        return Bot.delete_chat_photo(self, chat_id)

    @async_dec()
    def set_chat_title(self, chat_id, title):
        return Bot.set_chat_title(self, chat_id, title)

    @async_dec()
    def set_chat_description(self, chat_id, description):
        return Bot.set_chat_description(self, chat_id, description)

    @async_dec()
    def pin_chat_message(self, chat_id, message_id, disable_notification=False):
        return Bot.pin_chat_message(self, chat_id, message_id, disable_notification)

    @async_dec()
    def unpin_chat_message(self, chat_id, message_id=None):
        return Bot.unpin_chat_message(self, chat_id, message_id)

    @async_dec()
    def unpin_all_chat_message(self, chat_id):
        return Bot.unpin_all_chat_message(self, chat_id)

    @async_dec()
    def leave_chat(self, chat_id):
        return Bot.leave_chat(self, chat_id)

    @async_dec()
    def get_chat(self, chat_id):
        return Bot.get_chat(self, chat_id)

    @async_dec()
    def get_chat_administrators(self, chat_id):
        return Bot.get_chat_administrators(self, chat_id)

    @async_dec()
    def get_chat_member_count(self, chat_id):
        return Bot.get_chat_member_count(self, chat_id)

    @async_dec()
    def get_chat_member(self, chat_id, user_id):
        return Bot.get_chat_member(self, chat_id, user_id)

    @async_dec()
    def set_chat_sticker_set(self, chat_id, sticker_set_name):
        return Bot.set_chat_sticker_set(self, chat_id, sticker_set_name)

    @async_dec()
    def delete_chat_sticker_set(self, chat_id):
        return Bot.delete_chat_sticker_set(self, chat_id)

    @async_dec()
    def answer_callback_query(self, callback_query_id, text=None, show_alert=False, url=None, cache_time=None):
        return Bot.answer_callback_query(self, callback_query_id, text, show_alert, url, cache_time)

    @async_dec()
    def set_my_commands(self, commands, scope=None, language_code=None):
        return Bot.set_my_commands(self, commands, scope, language_code)

    @async_dec()
    def delete_my_commands(self, scope=None, language_code=None):
        return Bot.delete_my_commands(self, scope, language_code)

    @async_dec()
    def get_my_commands(self, scope=None, language_code=None):
        return Bot.get_my_commands(self, scope, language_code)

    @async_dec()
    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None,
                          entities=None, disable_web_page_preview=False, reply_markup=None):
        return Bot.edit_message_text(self, chat_id, chat_id, message_id, inline_message_id, parse_mode, entities,
                                     disable_web_page_preview, reply_markup)

    @async_dec()
    def edit_message_caption(self, chat_id=None, message_id=None, inline_message_id=None, caption=None, parse_mode=None,
                             caption_entities=None,
                             reply_markup=None):
        return Bot.edit_message_caption(self, chat_id, message_id, inline_message_id, caption, parse_mode,
                                        caption_entities, reply_markup)

    @async_dec()
    def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return Bot.edit_message_media(self, media, chat_id, message_id, inline_message_id, reply_markup)

    @async_dec()
    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        return Bot.edit_message_reply_markup(self, chat_id, message_id, inline_message_id, reply_markup)

    @async_dec()
    def stop_poll(self, chat_id, message_id, reply_markup=None):
        return Bot.stop_poll(self, chat_id, message_id, reply_markup)

    @async_dec()
    def delete_message(self, chat_id, message_id):
        return Bot.delete_message(self, chat_id, message_id)

    @async_dec()
    def send_sticker(self, chat_id, sticker, disable_notification=False, protect_content=False,
                     reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_sticker(self, chat_id, sticker, disable_notification, protect_content, reply_to_message_id,
                                allow_sending_without_reply, reply_markup)

    @async_dec()
    def get_sticker_set(self, name):
        return Bot.get_sticker_set(self, name)

    @async_dec()
    def upload_sticker_file(self, user_id, png_sticker):
        return Bot.upload_sticker_file(self, user_id, png_sticker)

    @async_dec()
    def create_new_sticker_set(self, user_id, name, title, emojis=None, png_sticker=None, tgs_sticker=None,
                               webm_sticker=None, contains_masks=False, mask_position=None):
        return Bot.create_new_sticker_set(self, user_id, name, title, emojis, png_sticker, tgs_sticker, webm_sticker,
                                          contains_masks, mask_position)

    @async_dec()
    def add_sticker_to_set(self, user_id, name, emojis, png_sticker=None, tgs_sticker=None, webm_sticker=None,
                           mask_position=None):
        return Bot.add_sticker_to_set(self, user_id, name, emojis, png_sticker, tgs_sticker, webm_sticker,
                                      mask_position)

    @async_dec()
    def set_sticker_position_in_set(self, sticker, position):
        return Bot.set_sticker_position_in_set(self, sticker, position)

    @async_dec()
    def delete_sticker_from_set(self, sticker):
        return Bot.delete_sticker_from_set(self, sticker)

    @async_dec()
    def set_sticker_set_thumb(self, name, user_id, thumb=None):
        return Bot.set_sticker_set_thumb(self, name, user_id, thumb)

    @async_dec()
    def answer_inline_query(self, inline_query_id, results, cache_time=300, is_personal=False, next_offset=None,
                            switch_pm_text=None, switch_pm_parameter=None):
        return Bot.answer_inline_query(self, inline_query_id, results, cache_time, is_personal, next_offset,
                                       switch_pm_text, switch_pm_parameter)

    @async_dec()
    def send_invoice(self, chat_id, title, description, payload, provider_token, currency, prices, max_tip_amount=None,
                     suggested_tip_amounts=None, start_parameter=None, provider_data=None, photo_url=None,
                     photo_size=None, photo_width=None, photo_height=None, need_name=False, need_phone_number=False,
                     need_email=False, need_shipping_address=False, send_phone_number_to_provider=False,
                     send_email_to_provider=False, is_flexible=False, disable_notification=False, protect_content=False,
                     reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_invoice(self, chat_id, title, description, payload, provider_token, currency, prices,
                                max_tip_amount, suggested_tip_amounts, start_parameter, provider_data, photo_url,
                                photo_size, photo_width, photo_height, need_name, need_phone_number, need_email,
                                need_shipping_address, send_phone_number_to_provider, send_email_to_provider,
                                is_flexible, disable_notification, protect_content, reply_to_message_id,
                                allow_sending_without_reply, reply_markup)

    @async_dec()
    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        return Bot.answer_shipping_query(self, shipping_query_id, ok, shipping_options, error_message)

    @async_dec()
    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        return Bot.answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message)

    @async_dec()
    def set_passport_data_errors(self, user_id, errors):
        return Bot.set_passport_data_errors(self, user_id, errors)

    @async_dec()
    def send_game(self, chat_id, game_short_name, disable_notification=False, protect_content=False,
                  reply_to_message_id=None, allow_sending_without_reply=False, reply_markup=None):
        return Bot.send_game(self, chat_id, game_short_name, disable_notification, protect_content, reply_to_message_id,
                             allow_sending_without_reply, reply_markup)

    @async_dec()
    def set_game_score(self, user_id, score, force=False, disable_edit_message=False, chat_id=None, message_id=None,
                       inline_message_id=None):
        return Bot.set_game_score(self, user_id, score, force, disable_edit_message, chat_id, message_id,
                                  inline_message_id)

    @async_dec()
    def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
        return Bot.get_game_high_scores(self, user_id, chat_id, message_id, inline_message_id)
