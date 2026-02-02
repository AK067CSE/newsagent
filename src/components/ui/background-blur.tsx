export default function BackgroundBlur() {
  return (
    <div className="absolute inset-0 overflow-hidden -z-10 bg-background min-h-screen">
      {/* Animated gradient orbs */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-purple-600/30 to-pink-600/30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute top-40 right-20 w-96 h-96 bg-gradient-to-r from-blue-600/25 to-cyan-600/25 rounded-full blur-3xl animate-bounce-slow"></div>
      <div className="absolute bottom-20 left-1/4 w-80 h-80 bg-gradient-to-r from-indigo-600/30 to-purple-700/30 rounded-full blur-3xl animate-float"></div>
      <div className="absolute bottom-40 right-10 w-64 h-64 bg-gradient-to-r from-pink-600/35 to-rose-600/35 rounded-full blur-3xl animate-float-reverse"></div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-gradient-to-r from-violet-600/20 to-purple-600/20 rounded-full blur-3xl animate-spin-slow"></div>

      {/* Grid pattern overlay */}
      <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
    </div>
  );
}
