"""HomeBot core module."""

from homebot import __version__, get_config
from homebot.core.admin import user_is_admin
from homebot.core.bot import get_bot_context
from homebot.core.logging import LOGI

def start(update, context):
	update.message.reply_text("Hi! I'm HomeBot, a bot written in Python by SebaUbuntu\n"
							  f"Version {__version__}\n"
							  "To see all the available modules, type /modules")

def modules(update, context):
	message = "Loaded modules:\n\n"
	modules = get_bot_context().modules
	for module in modules:
		message += f"{module.name}\n"
		message += f"Status: {modules[module]}\n"
		message += f"Commands: {', '.join([command.name for command in module.commands])}\n\n"
	update.message.reply_text(message)

def load(update, context):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to load modules")
		return

	try:
		module_name = update.message.text.split(' ', 1)[1]
	except IndexError:
		update.message.reply_text("Error: Module name not provided")
		return

	if module_name == "core":
		update.message.reply_text("Error: You can't load module used for loading/unloading modules")
		return

	bot_context = get_bot_context()
	modules = bot_context.modules
	for module in modules:
		if module_name == module.name:
			bot_context.load_module(module)
			update.message.reply_text(f"Module {module_name} loaded")
			return

	update.message.reply_text("Error: Module not found")

def unload(update, context):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to unload modules")
		return

	try:
		module_name = update.message.text.split(' ', 1)[1]
	except IndexError:
		update.message.reply_text("Error: Module name not provided")
		return

	if module_name == "core":
		update.message.reply_text("Error: You can't unload module used for loading/unloading modules")
		return

	bot_context = get_bot_context()
	modules = bot_context.modules
	for module in modules:
		if module_name == module.name:
			bot_context.unload_module(module)
			update.message.reply_text(f"Module {module_name} unloaded")
			return

	update.message.reply_text("Error: Module not found")

commands = [
	[start, ['start', 'help']],
	[modules, ['modules']],
	[load, ['load']],
	[unload, ['unload']]
]
