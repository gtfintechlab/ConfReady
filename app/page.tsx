import Image from "next/image";
import Navbar from "./components/Navbar";
import ModelCardGenerator from "./components/ModelCardGenerator";
import ModelCardPreview from "./components/ModelCardPreview";

export default function Home() {
  return (
    <main className="w-full">
      <Navbar />
      <div className=" w-full h-screen flex justify-center items-center flex-col">
      <ModelCardGenerator />
      </div>
      <div className="flex justify-center items-center w-full">
      <ModelCardPreview />
      </div>
    </main>
  );
}
