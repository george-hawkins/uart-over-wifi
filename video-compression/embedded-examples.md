Embedded video examples
=======================

Embedded AVIF and WebP animated images work very well but if you also require audio then your options are more limited.

This page display the result from trying various approaches. As of early April 2024, only the first two work. Perhaps with time some of the others will too.

See [`README.md`](README.md) for more details.

### Results using the drag-and-drop URL

Just leaving the URL, that you get from drag-and-drop with the GitHub editor, as it is.

Markdown:

```
https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606
```

Result:

https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606

---

Surrounding the URL with `<` and `>` to make clear it's a real link.

Markdown:

```
<https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606>
```

Result:

<https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606>

---

Surrounding the URL with back-ticks - unsurprisingly, this disables the GitHub magic that looks for such URLs when rendering the markdown.

Markdown:

```
`https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606`
```

Result:

`https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606`

---

Using the markdown image syntax with the URL.

Markdown:

```
![movie clip](https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606)
```

Result:

![movie clip](https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606)

---

Wrapping the URL up in an HTML `<video>` tag.

Markdown:

```
<video width="1280" height="720" autoplay loop muted>
  <source src="https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606" type="video/mp4" />
</video>
```

Note: the `<video>` tag would work if using e.g. GitHub Pages and the above comes from this SO [answer](https://stackoverflow.com/a/10415231/245602) which also explains why the rather unintuitive `muted` attribute is also required for an embedded looping video.

Result:

<video width="1280" height="720" autoplay loop muted>
  <source src="https://github.com/george-hawkins/uart-over-wifi/assets/5216161/089b501b-73d1-4859-8851-ebd2b2adc606" type="video/mp4" />
</video>

### The same but using the raw URL to the asset in the repo

Using the URL that one gets if one navigates to as an asset in your repo on GitHub and clicks the _Raw_ button.

Markdown:

```
https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4
```

Result:

https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4

---

Surrounding the URL with `<` and `>` to make clear it's a real link.

Markdown:

```
<https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4>
```

Result:

<https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4>

---

Surroundling the URL with back-ticks - unsurprisingly, this disables the GitHub magic that looks for such URLs when rendering the markdown.

Markdown:

```
`https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4`
```

Result:

`https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4`

---

Using the markdown image syntax with the URL.

Markdown:

```
![movie clip](https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4)
```

Result:

![movie clip](https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4)

---

Wrapping the URL up in an HTML `<video>` tag.

Markdown:

```
<video width="1280" height="720" autoplay loop muted>
  <source src="https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4" type="video/mp4" />
</video>
```

Result:

<video width="1280" height="720" autoplay loop muted>
  <source src="https://github.com/george-hawkins/uart-over-wifi/raw/master/video-compression/output-28-vs.mp4" type="video/mp4" />
</video>

### The same but using the asset filename (as one would with image markdown)

Just using the assets filename, i.e. `output-28-vs.mp4` rather than a URL.

Markdown:

```
output-28-vs.mp4
```

Result:

output-28-vs.mp4

---

Surrounding the URL with `<` and `>` to make clear it's a real link.

Markdown:

```
<output-28-vs.mp4>
```

Result:

<output-28-vs.mp4>

---

Surrounding the URL with back-ticks - unsurprisingly, this disables the GitHub magic that looks for such URLs when rendering the markdown.

Markdown:

```
`output-28-vs.mp4`
```

Result:

`output-28-vs.mp4`

---

Using the markdown image syntax with the URL.

Markdown:

```
![movie clip](output-28-vs.mp4)
```

Result:

![movie clip](output-28-vs.mp4)

---

Wrapping the URL up in an HTML `<video>` tag.

Markdown:

```
<video width="1280" height="720" autoplay loop muted>
  <source src="output-28-vs.mp4" type="video/mp4" />
</video>
```

Result:

<video width="1280" height="720" autoplay loop muted>
  <source src="output-28-vs.mp4" type="video/mp4" />
</video>
