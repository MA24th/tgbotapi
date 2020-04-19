# CHANGELOG

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
