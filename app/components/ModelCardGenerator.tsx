export default function ModelCardGenerator() {

    return (
        <div className="bg-zinc-100 h-fit w-fit rounded py-10 px-44 flex flex-col">
            <h1 className="text-2xl font-light text-center my-5">Build your Model Card</h1>
            <hr className="my-5"/>
            <h3 className="my-5">Name of Research Paper</h3>
            <input placeholder="Enter the name of the research paper" className="border-none outline-none py-2 px-12 rounded"/>

            <h3 className="my-5">Who are the authors? (Last Name, First Name)</h3>
            <input placeholder="Enter the name of the research paper" className="border-none outline-none py-2 px-12 rounded"/>

            <h3 className="my-5">Do you provide code? (Yes/No)</h3>
            <input placeholder="Enter the name of the research paper" className="border-none outline-none py-2 px-12 rounded"/>

            <button className="my-5 border-2 py-3 hover:bg-slate-400 hover:text-white">Export</button>
        </div>
    )
}