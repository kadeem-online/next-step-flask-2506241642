import path from "path";
import { defineConfig, loadEnv, type UserConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig(({ mode }): UserConfig => {
	const env = loadEnv(mode, process.cwd(), "");
	const is_dev: boolean = mode === "development";

	const config: UserConfig = {
		base: is_dev ? `http://localhost:5173` : `static/dist/`,
		root: path.resolve(__dirname, "src"),
		build: {
			outDir: path.resolve(__dirname, `app/static/dist`),
			emptyOutDir: true,
			sourcemap: is_dev ? "inline" : false,
			rollupOptions: {
				input: {
					main: path.resolve(__dirname, `src/main.ts`),
					style: path.resolve(__dirname, `src/styles.css`),
				},
			},
			chunkSizeWarningLimit: 500,
			manifest: true,
		},
		server: {
			port: 5173,
			strictPort: true,
		},
		plugins: [tailwindcss()],
	};

	return config;
});
