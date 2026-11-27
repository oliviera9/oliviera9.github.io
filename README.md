# Alain Olivier — International Mountain Leader

A responsive Jekyll website for hiking and trekking in the Dolomites. Published on GitHub Pages at https://oliviera9.github.io. The planned custom domain is `alainolivier.it`, which must be purchased before activation.

## Edit the site

- `_config.yml`: site name, description, canonical URL and public `email`. The public email is `oliviera9@gmail.com`. `contact_endpoint` supplies the form delivery address.
- `_data/activities.json`: dated activities with Italian and English descriptions; currently empty until real outings are supplied.
- `_data/experiences.json`: Italian (`it`) and English (`en`) walking experiences and descriptions. Review these proposed offerings before accepting bookings.
- `_data/contact.json`: professional registration, VAT, PEC, Instagram and WhatsApp details, transcribed from the supplied public Notion contact page.
- `_data/routes.json`: Italian and English homepage URLs.
- `_data/translations.json`: all Italian and English page text and SEO metadata.
- `_includes/home.html`: shared homepage structure for both languages.
- `_includes/contact-details.html`: professional details, email, PEC and social links in the homepage contact section.
- `it/index.html` and `en/index.html`: language entry pages.
- `index.html`: redirects the root to Italian, preserving incoming section links.
- `assets/css/main.css`: responsive layout and styles.
- `assets/images/hero.jpg`: supplied by the user as `IMG_4050.jpeg`, optimized to 2400 × 1350 for the homepage hero and social preview. Original photo unchanged.
- `assets/images/about.jpg`: user-supplied portrait from `IMG_0206 (2).jpeg`, optimized for the “Who I am” section. Original photo unchanged.
- `assets/images/mountain.jpg` (previous image, no longer displayed): Dolomites photography by [Andrei R. Popescu on Unsplash](https://unsplash.com/photos/majestic-mountains-loom-above-a-dense-forest-HBsmzKuGyuI), used under the Unsplash License.

No analytics or booking backend is included. Enquiries are sent to `oliviera9@gmail.com` through FormSubmit; no visitor data is stored by this Jekyll site. Fonts load from Google Fonts; the layout uses system fallbacks if unavailable.

## Upcoming activities

The homepage has a calendar list at `/it/#calendar` and `/en/#calendar`, grouped by month. Maintain dates in `_data/activities.json`. Only entries with `published: true` appear. The file currently contains `[]`, so visitors see a translated invitation to arrange a walk; there are no invented scheduled activities.

Use this example as a **draft**, replace its details with a real outing, then set `published` to `true`:

```json
[
  {
    "id": "summer-walk",
    "published": false,
    "date": "2027-06-12",
    "kind": "day",
    "status": "open",
    "it": {
      "title": "Titolo dell’uscita",
      "description": "Descrizione dell’itinerario.",
      "location": "Luogo di ritrovo",
      "difficulty": "Media",
      "duration": "5 ore"
    },
    "en": {
      "title": "Walk title",
      "description": "Description of the route.",
      "location": "Meeting location",
      "difficulty": "Moderate",
      "duration": "5 hours"
    }
  }
]
```

Dates must be quoted `YYYY-MM-DD` strings. Optionally add `end_date` for a multi-day activity; it stays visible through that date. `kind` must be `day`, `trek` or `custom`; `status` is `open` or `full`. Fully booked outings are labelled and allow enquiries about another date. IDs must be unique lowercase words joined by hyphens. Both language objects need all five text fields shown above.

Jekyll sorts and groups future activities when building. The browser also hides expired entries using the Europe/Rome date, including when returning to a tab, so a rebuild is not required just to remove yesterday’s outing. A rebuild is needed to add or edit an activity. Without JavaScript, the list reflects the last build date.

The information button selects the activity and its dates in the existing form, preserving the visitor’s message. The selected activity is included in the email; visitors can clear it. This requests information and does not reserve a place.

For a **local-only demo** with clearly labelled sample outings, including full and multi-day examples:

```sh
python3 scripts/preview_calendar.py
python3 -m http.server 4001 --directory .calendar-preview
```

Open http://127.0.0.1:4001/en/#calendar (or `/it/#calendar`). Demo data is built in a temporary source copy and written to ignored `.calendar-preview/`; the real data file stays unchanged. Standard site builds never include those samples.

Calendar checks:

```sh
node scripts/check_calendar.mjs
python3 scripts/check_calendar.py
```

They verify Rome date boundaries, sorting, month grouping, translations, expiry, unpublished drafts, multi-day dates and enquiry attributes. The normal language check also validates the real activity data before deployment.

## Enquiry form

The Italian and English homepages contain a native HTML POST form with name, reply email, activity, preferred dates, group size and message. Name, email and message are required. Experience links preselect the corresponding activity. Browser validation works without JavaScript, and submissions stay with the provider until it redirects to the localized confirmation page. The form has a honeypot and retains FormSubmit’s default CAPTCHA protection.

**One-time activation:** submit a test enquiry from the published website, then open the activation email sent by FormSubmit to `oliviera9@gmail.com` and confirm the address. Follow the provider’s prompts and resend a test enquiry after activation to verify delivery. The form must be activated before relying on it for enquiries. Automated checks do not send email or prove inbox delivery.

`contact_endpoint` in `_config.yml` controls the provider endpoint. To change the receiving address, update both `email` and `contact_endpoint`, deploy, and activate the new address. When the custom domain is connected, the provider may require a new activation for that origin. Localized confirmation URLs follow `url` and `baseurl` automatically.

The form explains to visitors that their details pass through FormSubmit for an enquiry reply. No newsletter subscription, tracking or automatic reply to the visitor is configured. See [FormSubmit setup](https://formsubmit.co/) for activation and delivery details.

## Languages

Italian is the default at `/it/`; English is at `/en/`. All contact details and the enquiry form are in the homepage’s `#contact` section. The old `/it/contatti/` and `/en/contact/` URLs redirect to the corresponding homepage contact section and are excluded from the sitemap. The visible IT / EN switch preserves the selected section. Both versions use the same layout, images and styles. Edit the matching language entry in the JSON data files to change text. Metadata, image descriptions, navigation, sitemap and alternate-language links are localized. No translation service, extra Jekyll plugin or backend is required.

## Local development

With Ruby and Bundler installed:

```sh
bundle install
bundle exec jekyll serve
```

Open http://127.0.0.1:4000. To build only, use `bundle exec jekyll build`. After building, run `python3 scripts/check_languages.py` to verify both language versions; deployment runs this check automatically.

## Deployment

Pushing `main` runs `.github/workflows/pages.yml`, which builds Jekyll and deploys the generated `_site` directory. In the repository's Settings → Pages, select **GitHub Actions** as the source.

After buying the domain, change `url` in `_config.yml` to `https://alainolivier.it`. The custom domain must also be configured in Settings → Pages as `alainolivier.it`; the Actions publishing method does not use `scripts/custom-domain.txt` or a `CNAME` file to set the repository domain. `_config.yml` supplies the public canonical URL.

At the domain's DNS provider, set these records:

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | oliviera9.github.io |

Replace conflicting web records for those same hosts while preserving mail and unrelated DNS records. DNS propagation and certificate issuance can take up to 24 hours. Enable **Enforce HTTPS** when GitHub makes it available.

See [GitHub's custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).
