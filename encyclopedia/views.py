from django.shortcuts import render, redirect
import markdown2
from django import forms
from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="Search Wiki", max_length=200)

class NewPage(forms.Form):
    title = forms.CharField(label="Page Title")
    md_content = forms.CharField(label="Markdown Content for Page", widget=forms.Textarea)

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

def search(request):
    form = SearchForm(request.GET)    
    matches = []
    if form.is_valid():
        entryname = form.cleaned_data["query"]
        entries = util.list_entries()
        matches = [e for e in entries if entryname.lower() in e.lower()]
        if not matches:
            return redirect("entry", entryname=entryname)
        elif len(matches) == 1 and entryname.lower() == matches[0].lower():
            return redirect("entry", entryname=matches[0])
        else:
            return render(request, "encyclopedia/search.html", {
                "matches": matches,
                "form": SearchForm()
            })

def newpage(request):
    return render(request, "encyclopedia/newpage.html", {
        "newpage": NewPage(),
        "form": SearchForm()
    })