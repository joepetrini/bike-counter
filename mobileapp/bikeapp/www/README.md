# Page Structure
* HTML in index.html
    * [Mustache](https://github.com/janl/mustache.js) js templates
    * Mobile pages split into id=tpl-[page] elements
* CSS in assets/css/bikecounter.css
* JS in bike.js and lib.js
    * bike.js has all app level variables, event hooks, and routing
    * lib.js has all application logic code

# Page Events
[Cordova Events](http://docs.phonegap.com/en/4.0.0/cordova_events_events.md.html)


# Cordova Info
[Install](http://cordova.apache.org/docs/en/4.0.0/guide_cli_index.md.html)


# Notes
To handle app exit, add last_active var, in load hook, if last_active diff from now
within X time and current session in effect auto load into that session in a paused state.
