import React from 'react'
import './About.css'
import about_image from '../../Assets/about2.jpg'
import play_icon from '../../Assets/play_icon.png'

const About = () => {
  return (
    <div className='about'>
      <div className='about-left'>
        <img src={about_image} alt="" className='about-img'/>
        <img src={play_icon} alt="" className='play-icon'/>
      </div>
      <div className='about-right'>
        <h3>About Formify</h3>
        <h2>Perfect your form one rep at a time</h2>
        <p>At Formify, we're dedicated to helping you get the most out of your workouts. Our platform uses Mediapipe to track your reps and correct your form, ensuring you exercise safely and effectively.</p>
        <p>Whether you're a beginner or an experienced athlete, our tool is designed to support you. We provide real-time tracking on your form, so you can focus on making progress with confidence.</p>
        <p>At the core of our mission is a commitment to improving the quality of your workouts. We understand that proper form is crucial for avoiding injuries and getting the most out of your exercises. That's why we've integrated cutting-edge technology that not only tracks your progress but also provides a tracker that can show you your form as you go. With our tracker, you can focus on pushing your limits while we handle the details that matter.</p>
        <p>Our easy-to-use interface lets you track your workouts effortlessly. With our advanced technology, you can stay on top of your fitness goals and push your limits.</p>
      </div>
    </div>
  )
}

export default About
