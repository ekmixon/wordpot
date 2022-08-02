from wordpot.plugins_manager import BasePlugin

class Plugin(BasePlugin):
    def run(self):
        # Initialize template vars dict 
        self.outputs['template_vars'] = {} 

        # First check if the file is wp-login.php
        if self.inputs['filename'] != 'wp-login' or self.inputs['ext'] != 'php':
            return 

        # Logic
        origin = self.inputs['request'].remote_addr

        if self.inputs['request'].method == 'POST':
            username = self.inputs['request'].form['log']
            password = self.inputs['request'].form['pwd']
            self.outputs[
                'log'
            ] = f'{origin} tried to login with username {username} and password {password}'

            self.outputs['log_json'] = self.to_json_log(username=username, password=password, plugin='badlogin')
            self.outputs['template_vars']['BADLOGIN'] = True
        else:
            self.outputs['log'] = f'{origin} probed for the login page'
            self.outputs['template_vars']['BADLOGIN'] = False
        self.outputs['template'] = 'wp-login.html'
        return
