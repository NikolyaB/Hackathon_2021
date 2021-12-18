@dp.message_handler(content_types=['text'])
            async def choose_subject(message):
                stage = db.Stage.query.filter_by(chat_id=call.from_user.id).all()[0]
                if stage.stage == 'login':
                    if message.text == code and stage.counter < 3:
                        await dp.bot.send_message(chat_id=message.chat.id,
                                                  text=message_menu,
                                                  reply_markup=keyboard.choose_course())
                        db.delete_stage(chat_id=call.from_user.id)
                        db.stage(chat_id=call.from_user.id,
                                 stage="choose_course")
                    if message.text != code:
                        if stage.counter == 3:
                            await dp.bot.send_message(chat_id=message.chat.id,
                                                      text="Превышено число попыток ввода пароля")
                            await dp.bot.send_message(chat_id=message.chat.id,
                                                      text="Выберите статус",
                                                      reply_markup=keyboard.choose_status())
                            db.delete_stage(chat_id=call.from_user.id)
                            db.stage(chat_id=call.from_user.id, stage="startы")

                        else:
                            stage.counter += 1
                            await dp.bot.send_message(chat_id=message.chat.id,
                                                      text="Неправильный пароль")


