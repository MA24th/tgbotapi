# CHANGELOG
## _v5.0_
### Run Your Own Bot API Server

- Bot API source code is now available at telegram-bot-api. You can now run your own Bot API server locally, boosting your bots' performance.
- Added the method logOut, which can be used to log out from the cloud Bot API server before launching your bot locally. You must log out the bot before running it locally, otherwise there is no guarantee that the bot will receive all updates.
- Added the method close, which can be used to close the bot instance before moving it from one local server to another.

### Transfer Bot Ownership
- You can now use @BotFather to transfer your existing bots to another Telegram account.

### Webhooks
- Added the parameter ip_address to the method setWebhook, allowing to bypass DNS resolving and use the specified fixed IP address to send webhook requests.
- Added the field ip_address to the class WebhookInfo, containing the current IP address used for webhook connections creation.
- Added the ability to drop all pending updates when changing webhook URL using the parameter drop_pending_updates in the methods setWebhook and deleteWebhook.

### Working with Groups
- The getChat request now returns the user's bio for private chats if available.
- The getChat request now returns the identifier of the linked chat for supergroups and channels, i.e. the discussion group identifier for a channel and vice versa.
- The getChat request now returns the location to which the supergroup is connected (see Local Groups). Added the class ChatLocation to represent the location.
- Added the parameter only_if_banned to the method unbanChatMember to allow safe unban.

### Working with Files
- Added the field file_name to the classes Audio and Video, containing the name of the original file.
- Added the ability to disable server-side file content type detection using the parameter disable_content_type_detection in the method sendDocument and the class inputMediaDocument.

### Multiple Pinned Messages
- Added the ability to pin messages in private chats.
- Added the parameter message_id to the method unpinChatMessage to allow unpinning of the specific pinned message.
- Added the method unpinAllChatMessages, which can be used to unpin all pinned messages in a chat.

### File Albums
- Added support for sending and receiving audio and document albums in the method sendMediaGroup.

### Live Locations
- Added the field live_period to the class Location, representing a maximum period for which the live location can be updated.
- Added support for live location heading: added the field heading to the classes Location, InlineQueryResultLocation, InputLocationMessageContent and the parameter heading to the methods sendLocation and editMessageLiveLocation.
- Added support for proximity alerts in live locations: added the field proximity_alert_radius to the classes Location, InlineQueryResultLocation, InputLocationMessageContent and the parameter proximity_alert_radius to the methods sendLocation and editMessageLiveLocation.
- Added the type ProximityAlertTriggered and the field proximity_alert_triggered to the class Message.
- Added possibility to specify the horizontal accuracy of a location. Added the field horizontal_accuracy to the classes Location, InlineQueryResultLocation, InputLocationMessageContent and the parameter horizontal_accuracy to the methods sendLocation and editMessageLiveLocation.

### Anonymous Admins
- Added the field sender_chat to the class Message, containing the sender of a message which is a chat (group or channel). For backward compatibility in non-channel chats, the field from in such messages will contain the user 777000 for messages automatically forwarded to the discussion group and the user 1087968824 (@GroupAnonymousBot) for messages from anonymous group administrators.
- Added the field is_anonymous to the class chatMember, which can be used to distinguish anonymous chat administrators.
- Added the parameter is_anonymous to the method promoteChatMember, which allows to promote anonymous chat administrators. The bot itself should have the is_anonymous right to do this. Despite the fact that bots can have the is_anonymous right, they will never appear as anonymous in the chat. Bots can use the right only for passing to other administrators.
- Added the custom title of an anonymous message sender to the class Message as author_signature.

### And More
- Added the method copyMessage, which sends a copy of any message.
- Maximum poll question length increased to 300.
- Added the ability to manually specify text entities instead of specifying the parse_mode in the classes InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaAudio, InputMediaDocument, InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultMpeg4Gif, InlineQueryResultVideo, InlineQueryResultAudio, InlineQueryResultVoice, InlineQueryResultDocument, InlineQueryResultCachedPhoto, InlineQueryResultCachedGif, InlineQueryResultCachedMpeg4Gif, InlineQueryResultCachedVideo, InlineQueryResultCachedAudio, InlineQueryResultCachedVoice, InlineQueryResultCachedDocument, InputTextMessageContent and the methods sendMessage, sendPhoto, sendVideo, sendAnimation, sendAudio, sendDocument, sendVoice, sendPoll, editMessageText, editMessageCaption.
- Added the fields google_place_id and google_place_type to the classes Venue, InlineQueryResultVenue, InputVenueMessageContent and the optional parameters google_place_id and google_place_type to the method sendVenue to support Google Places as a venue API provider.
- Added the field allow_sending_without_reply to the methods sendMessage, sendPhoto, sendVideo, sendAnimation, sendAudio, sendDocument, sendSticker, sendVideoNote, sendVoice, sendLocation, sendVenue, sendContact, sendPoll, sendDice, sendInvoice, sendGame, sendMediaGroup to allow sending messages not a as reply if the replied-to message has already been deleted.

### And Last but not Least
- Supported the new football and slot machine animations for the random dice. Choose between different animations (dice, darts, basketball, football, slot machine) by specifying the emoji parameter in the method sendDice.


## _v4.9_
- Added the new field via_bot to the Message object. You can now know which bot was used to send a message.
- Supported video thumbnails for inline GIF and MPEG4 animations.
- Supported the new basketball animation for the random dice. Choose between different animations (dice, darts, basketball) by specifying the emoji parameter in the method sendDice.

## _v4.8_
- Add explanations by specifying the parameters explanation and explanation_parse_mode in the method sendPoll.
- Added the fields explanation and explanation_entities to the Poll object.
- Supported timed polls that automatically close at a certain date and time. Set up by specifying the parameter open_period or close_date in the method sendPoll.
- Added the fields open_period and close_date to the Poll object.
- Supported the new darts animation for the dice mini-game. Choose between the default dice animation and darts animation by specifying the parameter emoji in the method sendDice.
- Added the field emoji to the Dice object.ed the ability to change thumbnails of sticker sets created by the bot using the method setStickerSetThumb.

## _v4.7_
- Added the method sendDice for sending a dice message, which will have a random value from 1 to 6. (Yes, we're aware of the “proper” singular of die. But it's awkward, and we decided to help it change. One dice at a time!)
- Added the field dice to the Message object.
- Added the method getMyCommands for getting the current list of the bot's commands.
- Added the method setMyCommands for changing the list of the bot's commands through the Bot API instead of @BotFather.
- Added the ability to create animated sticker sets by specifying the parameter tgs_sticker instead of png_sticker in the method createNewStickerSet.
- Added the ability to add animated stickers to sets created by the bot by specifying the parameter tgs_sticker instead of png_sticker in the method addStickerToSet.
- Added the field thumb to the StickerSet object.
- Added the ability to change thumbnails of sticker sets created by the bot using the method setStickerSetThumb.

## _v4.0_
- Supported Polls 2.0.
- Added the ability to send non-anonymous, multiple answer, and quiz-style polls: added the parameters is_anonymous, type, allows_multiple_answers, correct_option_id, is_closed options to the method sendPoll.
- Added the object KeyboardButtonPollType and the field request_poll to the object KeyboardButton.
- Added updates about changes of user answers in non-anonymous polls, represented by the object PollAnswer and the field poll_answer in the Update object.
- Added the fields total_voter_count, is_anonymous, type, allows_multiple_answers, correct_option_id to the Poll object.
- Bots can now send polls to private chats.
- Added more information about the bot in response to the getMe request: added the fields can_join_groups, can_read_all_group_messages and supports_inline_queries to the User object.
- Added the optional field language to the MessageEntity object.
- Added support for two new MessageEntity types, underline and strikethrough.
- Added support for nested MessageEntity objects. Entities can now contain other entities. If two entities have common characters then one of them is fully contained inside the other.
- Added vCard support when sharing contacts: added the field vcard to the objects Contact, InlineQueryResultContact, InputContactMessageContent and the method sendContact.
