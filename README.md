# GruaHelper

Simulador de puente grua (`index.html`), empaquetado como **Progressive Web App (PWA)**
para poder instalarse como una app en iOS y Android directamente desde el navegador,
sin pasar por App Store / Play Store.

## Estructura

```
index.html      # la app (single-file SPA, sin cambios de logica)
manifest.json   # metadatos de instalacion (nombre, iconos, colores, modo standalone)
sw.js           # service worker: cachea el app shell para uso offline
icons/          # iconos generados (192/512, maskable, apple-touch-icon, favicons)
```

No hay build step ni dependencias: son archivos estaticos que se sirven tal cual.

## Requisito clave: HTTPS

Los service workers (necesarios para "Agregar a pantalla de inicio" y el modo offline)
solo funcionan sobre **HTTPS** (o `localhost` en desarrollo). Cualquiera de las
opciones de hosting de abajo ya incluye HTTPS automatico.

## Opcion 1 — GitHub Pages (mas simple, gratis)

1. En GitHub: Settings del repo -> Pages -> Source: rama `main` (o la que uses), carpeta `/root`.
2. Guarda. GitHub publica el sitio en `https://<usuario>.github.io/<repo>/`.
3. Si el sitio no queda en la raiz del dominio (por ejemplo queda en `/an/`), ajusta
   las rutas absolutas `/manifest.json`, `/sw.js`, `/icons/...` en `index.html`,
   `manifest.json` y `sw.js` para que sean relativas (`./manifest.json`, etc.) o
   antepone el subpath.

## Opcion 2 — Netlify / Vercel (gratis, dominio propio opcional)

1. Crea cuenta en netlify.com o vercel.com y conecta este repositorio de GitHub.
2. Build command: (vacio). Publish/output directory: `/` (raiz del repo).
3. Deploy. Te dan una URL HTTPS al instante (`https://tu-app.netlify.app`),
   y puedes conectar un dominio propio despues desde el panel.

Esta es la opcion recomendada si no quieres administrar un servidor.

## Opcion 3 — Servidor propio (VPS con Nginx)

Si prefieres tu propio servidor (ej. una VPS en DigitalOcean/Linode/AWS):

1. Sube los archivos del repo a, por ejemplo, `/var/www/gruahelper/`.
2. Configura Nginx:

   ```nginx
   server {
     listen 80;
     server_name tu-dominio.com;
     root /var/www/gruahelper;
     index index.html;

     location / {
       try_files $uri $uri/ /index.html;
     }

     location /sw.js {
       add_header Cache-Control "no-cache";
     }
   }
   ```

3. Instala un certificado HTTPS gratis con Certbot:

   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d tu-dominio.com
   ```

4. Certbot reconfigura Nginx para servir por HTTPS (puerto 443) automaticamente.

## Instalar la app en el celular

**Android (Chrome):**
1. Abre la URL del sitio.
2. Menu (⋮) -> "Agregar a pantalla de inicio" / "Instalar app".
3. Queda como un icono mas, abre en pantalla completa (sin barra del navegador).

**iOS (Safari — obligatorio usar Safari, no Chrome):**
1. Abre la URL del sitio en Safari.
2. Boton de compartir (cuadrado con flecha hacia arriba) -> "Agregar a pantalla de inicio".
3. Queda como un icono mas, abre en pantalla completa.

## Actualizar la app despues de publicada

El service worker cachea los archivos. Cuando cambies `index.html`, sube el cambio
y sube tambien la version del cache en `sw.js` (constante `CACHE_NAME`, ej.
`gruahelper-v2`) para forzar a los usuarios a descargar la version nueva la
siguiente vez que abran la app.

## Si mas adelante quieres subirla a App Store / Play Store

Esta PWA cubre "instalar como app" desde el navegador. Si en el futuro necesitas
presencia en las tiendas oficiales (App Store / Play Store), se puede envolver
este mismo `index.html` con [Capacitor](https://capacitorjs.com/) sin reescribir
la logica de la app. Es un paso aparte, no necesario para lo pedido ahora.
