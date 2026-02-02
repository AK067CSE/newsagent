/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
        gradient: {
          "0%, 100%": {
            backgroundPosition: "0% 50%",
          },
          "50%": {
            backgroundPosition: "100% 50%",
          },
        },
        float: {
          "0%": { transform: "translateY(0px) translateX(0px)" },
          "25%": { transform: "translateY(-20px) translateX(10px)" },
          "50%": { transform: "translateY(-10px) translateX(-10px)" },
          "75%": { transform: "translateY(-30px) translateX(5px)" },
          "100%": { transform: "translateY(0px) translateX(0px)" },
        },
        glow: {
          "0%, 100%": { opacity: 0.8, filter: "saturate(100%) brightness(100%)" },
          "50%": { opacity: 1, filter: "saturate(120%) brightness(120%)" },
        },
        pulse: {
          "0%, 100%": { opacity: 1 },
          "50%": { opacity: 0.7 },
        },
        "bounce-slow": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        "float-reverse": {
          "0%": { transform: "translateY(0px) translateX(0px)" },
          "25%": { transform: "translateY(20px) translateX(-10px)" },
          "50%": { transform: "translateY(10px) translateX(10px)" },
          "75%": { transform: "translateY(30px) translateX(-5px)" },
          "100%": { transform: "translateY(0px) translateX(0px)" },
        },
        "spin-slow": {
          "0%": { transform: "translate(-50%, -50%) rotate(0deg)" },
          "100%": { transform: "translate(-50%, -50%) rotate(360deg)" },
        },
        "pulse-slow": {
          "0%, 100%": { opacity: 0.3, transform: "scale(1)" },
          "50%": { opacity: 0.6, transform: "scale(1.05)" },
        },
        "float-slow": {
          "0%": { transform: "translateY(0px) translateX(0px)" },
          "25%": { transform: "translateY(-15px) translateX(5px)" },
          "50%": { transform: "translateY(-5px) translateX(-5px)" },
          "75%": { transform: "translateY(-20px) translateX(3px)" },
          "100%": { transform: "translateY(0px) translateX(0px)" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        gradient: "gradient 8s linear infinite",
        float: "float 15s ease-in-out infinite",
        glow: "glow 4s ease-in-out infinite",
        pulse: "pulse 3s ease-in-out infinite",
        "bounce-slow": "bounce-slow 3s ease-in-out infinite",
        "float-reverse": "float-reverse 12s ease-in-out infinite",
        "spin-slow": "spin-slow 20s linear infinite",
        "pulse-slow": "pulse-slow 4s ease-in-out infinite",
        "float-slow": "float-slow 18s ease-in-out infinite",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
