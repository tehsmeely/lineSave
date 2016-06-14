import sublime, sublime_plugin, string, os.path

 

settings_filename = "LineSave.sublime-settings"

save_path = "save_path"

 

class LineSaveCommand(sublime_plugin.TextCommand):

            def run(self, edit):
                        print "Line Save"
                        ##get the region of the first line
                        reg = self.view.line(0)
                        #get the text of the first line
                        lineStr = self.view.substr(reg)
                        #filter string for inavlid chars
                        # this approach from http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
                        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
                        saveStr = ''.join(c for c in lineStr if c in valid_chars)
                        print saveStr
                        self.save(saveStr)

            def save(self, saveStr):
                        ##this saving method comes from a package: CreateSavePrompt
                        # found here: https://github.com/cellis/CreateSavePrompt/blob/master/CreateSavePrompt.py
                        print "saving", saveStr

                        settings = sublime.load_settings(settings_filename)
                        path = settings.get(save_path, "/")
                        #location = "D:\\Library\\Documents\\sublTest\\" + saveStr
                        location = os.path.join(path, saveStr)
                        if os.path.isfile(location):
                                    if not sublime.ok_cancel_dialog("The save file {0} already exists.\nOverwrite?".format(location)):
                                                return

                        with open(location, 'w') as f:
                                    print "file opened"
                                    f.write(self.view.substr(sublime.Region(0, self.view.size())))
                        self.view.set_scratch(True)
                        print "closing file"
                        self.view.window().run_command('close')
                        print "reopening file"
                        newView = self.window().open_file(location)
                        sublime.status_message("   Saved file in {0}".format(location))
                        # need to force update of window for reload, a simple click by user works but its not ideal

                        # this doesnt actually help
                        self.window().focus_view(newView)

            def window(self):
                        return sublime.active_window()
