import { defineConfig } from "vite"; // ✅ Keep only one
import react from "@vitejs/plugin-react";



export default defineConfig({
  plugins: [react()],

  build: {
    emptyOutDir: false,
    outDir: "dist",
  }
});
