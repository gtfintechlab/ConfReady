import Image from "next/image";
import Navbar from "./components/Navbar";
import ModelCardGenerator from "./components/ModelCardGenerator";

export default function Home() {
  return (
    <main className="h-dvh w-full">
      <Navbar />
      <div className="h-full flex justify-center items-center">
      <ModelCardGenerator />
      </div>
    </main>
  );
}
