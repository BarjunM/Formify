import { useEffect, useState } from "react";
import Background from "./Components/Background/Background";
import Navbar from "./Components/Navbar/Navbar";
import Hero from "./Components/Hero/Hero";
import About from "./Components/About/About";
import Title from "./Components/Title/Title";
import Contact from "./Components/Contact/Contact";
import FileUpload from "./Components/FileUpload/FileUpload";

const App = () => {
  let heroData = [
    {text1:"Perfect",text2:"your form"},
    {text1:"Indulge",text2:"your workout"},
    {text1:"Give in to",text2:"your passions"},
  ]
  const [heroCount,setHeroCount] = useState(0);
  const [playStatus,setPlayStatus] = useState(false);

  useEffect(()=>{
    setInterval(() => {
      setHeroCount((count)=>{return count===2?0:count+1})
    }, 3000);
  },[])

  return (
    <div>
      <Background playStatus={playStatus} heroCount={heroCount}/>
      <Navbar/>
      <Hero
        setPlayStatus={setPlayStatus}
        heroData={heroData[heroCount]}
        heroCount={heroCount}
        setHeroCount={setHeroCount}
        playStatus={playStatus}
      />
      <About/>
      <FileUpload/>
      <Title subTitle= 'Contact Us' title='Get in Touch'/>
      <Contact/>
    </div>
  )
}

export default App

