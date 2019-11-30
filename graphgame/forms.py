from django import forms


class GraphGameForm(forms.Form):
    class Media:
        js = ('graphgame/static/canvas.js',)

    g_name = forms.CharField(label='Graph name', max_length=256)
