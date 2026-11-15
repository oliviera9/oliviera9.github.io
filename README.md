# Alain Olivier — International Mountain Leader

A responsive Jekyll website for hiking and trekking in the Dolomites. Published on GitHub Pages at https://oliviera9.github.io. The planned custom domain is `alainolivier.it`, which must be purchased before activation.

## Edit the site

- `_config.yml`: site name, description, canonical URL and public `email`. The email is deliberately blank until a real address is supplied. Adding it enables the contact links.
- `_data/experiences.json`: Italian (`it`) and English (`en`) walking experiences and descriptions. Review these proposed offerings before accepting bookings.
- `_data/translations.json`: all Italian and English page text and SEO metadata.
- `_includes/home.html`: shared page structure for both languages.
- `it/index.html` and `en/index.html`: language entry pages.
- `index.html`: redirects the root to Italian, preserving incoming section links.
- `assets/css/main.css`: responsive layout and styles.
- `assets/images/mountain.jpg`: Dolomites photography by [Andrei R. Popescu on Unsplash](https://unsplash.com/photos/majestic-mountains-loom-above-a-dense-forest-HBsmzKuGyuI), used under the Unsplash License.

No analytics, booking backend or visitor data storage is included. Contact uses email once configured. Fonts load from Google Fonts; the layout uses system fallbacks if unavailable.

## Languages

Italian is the default at `/it/`; English is at `/en/`. The visible IT / EN switch preserves the selected section. Both versions use the same layout, images and styles. Edit the matching language entry in the JSON data files to change text. Metadata, image descriptions, navigation, sitemap and alternate-language links are localized. No translation service, extra Jekyll plugin or backend is required.

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
