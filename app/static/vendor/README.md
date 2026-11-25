# Bundled QR dependencies

These browser libraries are vendored so scanning and generation do not depend on a CDN or upload camera frames. Original code is retained, with licenses alongside it.

| File | Upstream | Source blob SHA | License |
| --- | --- | --- | --- |
| `jsQR.js` | https://github.com/cozmo/jsQR/blob/master/dist/jsQR.js | `99ea9df26907009e5553233ffe03c529c1521739` | Apache-2.0; `jsQR-LICENSE.txt` |
| `qrcode.js` | https://github.com/kazuhikoarase/qrcode-generator/blob/master/js/dist/qrcode.js | `df13f829bf41f36b82f0ed85751ed3b4c39cfeb8` | MIT; `qrcode-LICENSE.txt` |

Retrieved through GitHub on 25 November 2026. No npm package installation is needed at runtime. Permanent payload format is `BTG:ASSET:<ID>`. A four-module quiet zone and medium error correction are used in the prepared sheets. Software roundtrip and simulated video tests do not establish phone compatibility or printed-label robustness.
