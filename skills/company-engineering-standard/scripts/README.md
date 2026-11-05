# Document generation helper scripts

These helpers do **not** turn a document description into DOCX by themselves.

1. Read `../SKILL.md`, the applicable `../references/` and `../prompts/` files.
2. Author the Node.js file for the particular document (requires a runtime with Node and `docx` installed in that JS project's local node_modules).
3. Execute: `python generate_docx.py --type BRD --project "Example" --script /absolute/path/generate.js --output /path/to/output`.
4. Validate separately: `python validate_document.py /path/to/output/file.docx`.

Do not run untrusted JS generators. The wrapper executes `--script` as code. No company-approved `.docx` template binary is included in this package. `template_loader.py` helps prepare structured inputs; `style_apply.py` and `validate_document.py` are separate post-processing/inspection utilities. For optional Google API access install `requirements-google.txt` at the package root and provide **your own** OAuth client credentials. Never commit `credentials.json` or `token.json`.

### Optional authenticated Google Docs retrieval

If you explicitly authorize the Google API helper, store your own OAuth client file **outside the project** (default `~/.config/innotech/google/credentials.json`), then install `requirements-google.txt`. The first manually invoked login writes `~/.config/innotech/google/token.json` (0600 on POSIX). Override those paths via `INNOTECH_GOOGLE_CREDENTIALS_FILE` and `INNOTECH_GOOGLE_TOKEN_FILE`. Nothing is shipped with credentials; never commit the local token or client secret.
