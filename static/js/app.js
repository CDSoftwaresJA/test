
Vue.component("app-header", {
  template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
        <a class="navbar-brand" href="/">Photogram</a>
       <div>
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
          <router-link class="nav-link" to="/explore">Explore<span class="sr-only">(current)</span></router-link>
          </li>
        <li class="nav-item">
           <router-link class="nav-link" to="/users/0">My Profile<span class="sr-only">(current)</span></router-link>
        </li>
             <li class="nav-item">
           <router-link class="nav-link" to="/posts/new">New Post<span class="sr-only">(current)</span></router-link>
        </li>
 
        <li class="nav-item">
           <router-link class="nav-link" to="/">Logout<span class="sr-only">(current)</span></router-link>
        </li>
        </ul>
      </div>
    </nav>

    `,
  data: function(){
    return {
      div:"",
      id:0
    }
  },
  created:async function(){
        const session = await fetch('/api/session');
       	const data = await session.json();
       	if (data.message!=0){
       	  this.id=data.message;
       	}
        
  },


});


const Home = Vue.component("home", {
  template: `
  <div class="logingrid">
  <br>
  <br>
  <br>
  <br>
  <div class="loginimage">
  
    <img src="/static/images/karl-lee-ojb8uwDDXu8-unsplash.jpg"/>
  </div>
  <div class="loginbox">
  
    <h2>Photogram</h2>
    <router-link to="/register" tag="button">Register</router-link>
    <router-link to="/login" tag="button">Login</router-link>
  </div>
  </div>
   `,
  data: function () {
    return {};
  },
  created:async function(){
        const session = await fetch('/api/auth/logout');
       	const data = await session.json();
     
  }
});



const Register = Vue.component("register-form", {
   methods: {
            async  get() { 
         const res = await fetch('/api/users');
  				const data = await res.json();
          //alert(JSON. stringify(data));
              },
              
            async post() {
      let headers = {
    'Content-Type': 'application/json'
  };      
       var obj =  {
    biography: this.biography, 
    email: this.email, 
    first_name: this.fname, 
    last_name:this.lname, 
    location: this.location, 
    password: this.password, 
    username: this.username
    };
      	const request = new Request(
        		'/api/users/register',
        {
          method: "POST",
          headers,
          body: JSON.stringify(obj)

        },

      );
      const res = await fetch(request);
        const data = await res.json();
        router.push({ path: '/login' });
        alert(JSON. stringify(data));
            
              
            }     
,
          async postPhoto() {
              const formData  = new FormData();
              formData.append("image",this.photo);
  let headers2 = {
    'Content-Type': 'multipart/form-data'
  };
    const request = new Request(
        		'/api/users/addphoto/'+this.username,
        {
          method: "POST",
          headers2,
          body: formData

        },
      );
        const res = await fetch(request);
        const data = await res.json();
        alert(JSON. stringify(data));
            
              
            }     

        } ,

        

  template: 

  ` 
  <div
  <br>
  <br>
  <br>
  <br>

  <input v-model="username" placeholder="username">
  <br>
  <input v-model="fname" placeholder="fname">
  <br>
  <input v-model="lname" placeholder="lname">
  <br>
  <input v-model="password" placeholder="password">
  <br>
  <input v-model="biography" placeholder="biography">
  <br>
    <input v-model="location" placeholder="location">
  <br>
      <input v-model="email" placeholder="email">
  <br>
  <input v-model="photo" type="file">
  <br>
  <button v-on:click="postPhoto">Upload Photo</button>  

  <button v-on:click="post">Register</button>  
  </div>
`
});

const Login = Vue.component("login-form", {
  template: 
  ` 
  <div>
  <br>
  <br>
  <br>
  <br>
  <input v-model="username" placeholder="username">
  <br>
  <input v-model="password" placeholder="password">
  <br>
  <button v-on:click="post">Login</button>  
  </div>
`,
methods: {
  async post(){
          let headers = {
    'Content-Type': 'application/json'
  };

           var obj =  {
    password: this.password, 
    username: this.username
  };
      	const request = new Request(
        		'/api/auth/login',
        {
          method: "POST",
          headers,
          body: JSON.stringify(obj)

        },

      );
        const res = await fetch(request);
        const data = await res.json();
        const json = JSON.stringify(data);
        alert(json);
        router.push({ path: '/explore' });
  }
}
});
const Posts = Vue.component("post-form", {
  template: 
  ` 
  <div>
    <br>
  <br>
  <br>
  <br>

  <br>
      <input v-model="email" placeholder="email">
  <br>
  <input v-model="photo" type="file">
  <br>
  <button v-on:click="postPhoto">Upload Photo</button>  
  </div>
`,
methods: {
  async post(){
          let headers = {
    'Content-Type': 'application/json'
  };

           var obj =  {
    password: this.password, 
    username: this.username
  };
      	const request = new Request(
        		'/api/auth/login',
        {
          method: "POST",
          headers,
          body: JSON.stringify(obj)

        },

      );
        const res = await fetch(request);
        const data = await res.json();
        const json = JSON.stringify(data);
        alert(json);
        router.push({ path: '/explore' });
  }
}
});


const Explore = Vue.component("explore", {
  
  created:async function(){
        const res = await fetch('/api/posts');
  				const data = await res.json();
          this.posts = data;
 
  },
  
  data: function () {
    return {
    posts: []
  }
 },

  template: 
  ` 
  <div>
  <br>
  <br>
  <br>
  <br>
  <div v-for="post in posts">
  {{ post.user_id }}
  <br>
  {{ post.photo }}
  <br>
  {{ post.caption }}
  <br>
  {{ post.created_on }}
   <br>
  </div>
  </div>
`,
methods: {
      async  get() { 
         const res = await fetch('/api/posts');
  				const data = await res.json();
          alert(JSON. stringify(data));
          this.posts = JSON. stringify(data);
          
      }
}
});
const Users = Vue.component("users", {
  created:async function(){
        const res = await fetch('/api/user/'+this.$route.params.id);
  	   const res2 = await fetch('/api/users/'+this.$route.params.id+'/posts');
  				const data = await res.json();
          const data2 = await res2.json();
          this.info = data;
          this.posts = data;

  },
  
  data: function () {
    return {
    info: '',
    posts: ''
  }
 },
  template: 
  ` 
   <div>
  <br>
  <br>
  <br>
  <br>

  {{ info.first_name }} {{ info.last_name }}
  <br>
  <img v-bind:src="info.photo" height=50 width=50> 
  <br>
  {{ info.location }}
  <br>
  {{ info.biography }}
  <br>
  <button v-on:click="follow">Follow</button>  
  
  {{ posts }}
  </div>
`,
methods: {
      async  get() { 
         const res = await fetch('/api/info');
  				const data = await res.json();
          alert(JSON. stringify(data));
          this.info = JSON. stringify(data);
          
      }
}
});
const NotFound = Vue.component("not-found", {
  template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
  data: function () {
    return {};
  },
});

const router = new VueRouter({
  mode: "history",
  routes: [
    { path: "/", component: Home },
    { path: "/register", component: Register },
    { path: "/login", component: Login },
    { path: "/explore", component: Explore },
    { path: "/posts/new", component: Posts },
    { path: "/users/:id", component: Users, props: true  },
    { path: "*", component: NotFound },
  ],
});

// Instantiate our main Vue Instance
let app = new Vue({
  el: "#app",
  router,
});
