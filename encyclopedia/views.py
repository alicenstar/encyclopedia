from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from django import forms
from . import util

class SearchForm(forms.Form):
    query = forms.CharField(name="Search Query", inital="Query here...", max_length=200)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, entryname):
    getentry = util.get_entry(entryname)
    markdowner = markdown2.Markdown()
    if getentry is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": entryname,
            "html": markdowner.convert(getentry),
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "html": "<h1>Search Not Found</h1><p>Sorry, but no entries matched your query.</p>",
            "form": SearchForm()
        })

def search(request, data):
    query = SearchForm(request.GET)
    matches = []
    if query.is_valid():
        entryname = query.cleaned_data["query"]
        
    return HttpResponseRedirect(reverse("entry"))