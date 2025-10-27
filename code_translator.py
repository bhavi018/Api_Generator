"""
Multi-Language Code Generator
Translates FastAPI CRUD operations to different programming languages
"""


def generate_java_spring_code(org_id: str, org_name: str) -> str:
    """Generate Spring Boot REST API code"""
    return f"""
// {org_name} User Management API - Spring Boot

package com.{org_name.lower().replace(' ', '')}.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.Optional;

@SpringBootApplication
public class Application {{
    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
}}

// Entity Model
@Entity
@Table(name = "users")
class User {{
    @Id
    @Column(name = "org_user_id")
    private String orgUserId;
    
    @Column(name = "org_id")
    private String orgId;
    
    @Column(nullable = false)
    private String name;
    
    @Column(name = "contact_no")
    private String contactNo;
    
    @Column(name = "employee_code")
    private String employeeCode;
    
    @Column(name = "created_date")
    private LocalDateTime createdDate;
    
    @Column(name = "valid_till")
    private LocalDateTime validTill;
    
    // Getters and Setters
    public String getOrgUserId() {{ return orgUserId; }}
    public void setOrgUserId(String orgUserId) {{ this.orgUserId = orgUserId; }}
    
    public String getOrgId() {{ return orgId; }}
    public void setOrgId(String orgId) {{ this.orgId = orgId; }}
    
    public String getName() {{ return name; }}
    public void setName(String name) {{ this.name = name; }}
    
    public String getContactNo() {{ return contactNo; }}
    public void setContactNo(String contactNo) {{ this.contactNo = contactNo; }}
    
    public String getEmployeeCode() {{ return employeeCode; }}
    public void setEmployeeCode(String employeeCode) {{ this.employeeCode = employeeCode; }}
}}

// Repository Interface
@Repository
interface UserRepository extends JpaRepository<User, String> {{
    Optional<User> findByOrgUserIdAndOrgId(String orgUserId, String orgId);
    List<User> findByOrgId(String orgId);
}}

// REST Controller
@RestController
@RequestMapping("/api/org/{org_id}/users")
public class UserController {{
    
    @Autowired
    private UserRepository userRepository;
    
    // Create User
    @PostMapping("/")
    public ResponseEntity<User> createUser(@PathVariable("org_id") String orgId, 
                                          @RequestBody User user,
                                          @RequestHeader("Authorization") String token) {{
        // Add authentication logic here
        user.setOrgId(orgId);
        user.setCreatedDate(LocalDateTime.now());
        User savedUser = userRepository.save(user);
        return new ResponseEntity<>(savedUser, HttpStatus.CREATED);
    }}
    
    // Get User
    @GetMapping("/{{userId}}")
    public ResponseEntity<User> getUser(@PathVariable("org_id") String orgId,
                                       @PathVariable("userId") String userId) {{
        Optional<User> user = userRepository.findByOrgUserIdAndOrgId(userId, orgId);
        return user.map(ResponseEntity::ok)
                   .orElse(ResponseEntity.notFound().build());
    }}
    
    // Update User
    @PutMapping("/{{userId}}")
    public ResponseEntity<User> updateUser(@PathVariable("org_id") String orgId,
                                          @PathVariable("userId") String userId,
                                          @RequestBody User updatedUser) {{
        Optional<User> existingUser = userRepository.findByOrgUserIdAndOrgId(userId, orgId);
        if (existingUser.isPresent()) {{
            User user = existingUser.get();
            user.setName(updatedUser.getName());
            user.setContactNo(updatedUser.getContactNo());
            user.setEmployeeCode(updatedUser.getEmployeeCode());
            User savedUser = userRepository.save(user);
            return ResponseEntity.ok(savedUser);
        }}
        return ResponseEntity.notFound().build();
    }}
    
    // Delete User
    @DeleteMapping("/{{userId}}")
    public ResponseEntity<Void> deleteUser(@PathVariable("org_id") String orgId,
                                          @PathVariable("userId") String userId) {{
        Optional<User> user = userRepository.findByOrgUserIdAndOrgId(userId, orgId);
        if (user.isPresent()) {{
            userRepository.delete(user.get());
            return ResponseEntity.noContent().build();
        }}
        return ResponseEntity.notFound().build();
    }}
}}

// application.properties
/*
spring.datasource.url=jdbc:postgresql://localhost:5432/{org_name.lower()}
spring.datasource.username=admin
spring.datasource.password=password
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
server.port=8080
*/
"""


def generate_nodejs_express_code(org_id: str, org_name: str) -> str:
    """Generate Node.js Express REST API code"""
    return f"""
// {org_name} User Management API - Node.js + Express

const express = require('express');
const {{ Sequelize, DataTypes }} = require('sequelize');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const app = express();
app.use(express.json());

// Database Configuration
const sequelize = new Sequelize('database', 'username', 'password', {{
    host: 'localhost',
    dialect: 'postgres',
    logging: false
}});

// User Model
const User = sequelize.define('User', {{
    orgUserId: {{
        type: DataTypes.STRING,
        primaryKey: true,
        field: 'org_user_id'
    }},
    orgId: {{
        type: DataTypes.STRING,
        allowNull: false,
        field: 'org_id'
    }},
    name: {{
        type: DataTypes.STRING,
        allowNull: false
    }},
    contactNo: {{
        type: DataTypes.STRING,
        field: 'contact_no'
    }},
    employeeCode: {{
        type: DataTypes.STRING,
        field: 'employee_code'
    }},
    createdDate: {{
        type: DataTypes.DATE,
        defaultValue: Sequelize.NOW,
        field: 'created_date'
    }},
    validTill: {{
        type: DataTypes.DATE,
        field: 'valid_till'
    }}
}}, {{
    tableName: 'users',
    timestamps: false
}});

// Authentication Middleware
const authenticateToken = (req, res, next) => {{
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {{
        return res.status(401).json({{ error: 'Access token required' }});
    }}
    
    jwt.verify(token, 'your-secret-key', (err, user) => {{
        if (err) return res.status(403).json({{ error: 'Invalid token' }});
        req.user = user;
        next();
    }});
}};

// Routes

// Create User
app.post('/api/org/:orgId/users/', authenticateToken, async (req, res) => {{
    try {{
        const {{ orgId }} = req.params;
        const userData = {{ ...req.body, orgId }};
        
        const user = await User.create(userData);
        res.status(201).json({{ message: 'User created', user }});
    }} catch (error) {{
        res.status(400).json({{ error: error.message }});
    }}
}});

// Get User
app.get('/api/org/:orgId/users/:userId', async (req, res) => {{
    try {{
        const {{ orgId, userId }} = req.params;
        
        const user = await User.findOne({{
            where: {{ orgUserId: userId, orgId }}
        }});
        
        if (!user) {{
            return res.status(404).json({{ error: 'User not found' }});
        }}
        
        res.json(user);
    }} catch (error) {{
        res.status(500).json({{ error: error.message }});
    }}
}});

// Update User
app.put('/api/org/:orgId/users/:userId', authenticateToken, async (req, res) => {{
    try {{
        const {{ orgId, userId }} = req.params;
        
        const [updated] = await User.update(req.body, {{
            where: {{ orgUserId: userId, orgId }}
        }});
        
        if (!updated) {{
            return res.status(404).json({{ error: 'User not found' }});
        }}
        
        const updatedUser = await User.findOne({{
            where: {{ orgUserId: userId, orgId }}
        }});
        
        res.json({{ message: 'User updated', user: updatedUser }});
    }} catch (error) {{
        res.status(400).json({{ error: error.message }});
    }}
}});

// Delete User
app.delete('/api/org/:orgId/users/:userId', authenticateToken, async (req, res) => {{
    try {{
        const {{ orgId, userId }} = req.params;
        
        const deleted = await User.destroy({{
            where: {{ orgUserId: userId, orgId }}
        }});
        
        if (!deleted) {{
            return res.status(404).json({{ error: 'User not found' }});
        }}
        
        res.json({{ message: 'User deleted' }});
    }} catch (error) {{
        res.status(500).json({{ error: error.message }});
    }}
}});

// Login/Token Generation
app.post('/token', async (req, res) => {{
    const {{ orgId, role }} = req.body;
    const token = jwt.sign({{ orgId, role }}, 'your-secret-key', {{ expiresIn: '1h' }});
    res.json({{ access_token: token, token_type: 'bearer' }});
}});

// Initialize Database and Start Server
sequelize.sync().then(() => {{
    app.listen(8000, () => {{
        console.log('Server running on http://localhost:8000');
    }});
}});

// package.json
/*
{{
  "name": "{org_name.lower().replace(' ', '-')}-api",
  "version": "1.0.0",
  "dependencies": {{
    "express": "^4.18.2",
    "sequelize": "^6.35.0",
    "pg": "^8.11.3",
    "jsonwebtoken": "^9.0.2",
    "bcrypt": "^5.1.1"
  }}
}}
*/
"""


def generate_csharp_dotnet_code(org_id: str, org_name: str) -> str:
    """Generate C# .NET Core Web API code"""
    return f"""
// {org_name} User Management API - ASP.NET Core

using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace {org_name.replace(' ', '')}.API
{{
    // Startup.cs / Program.cs
    public class Program
    {{
        public static void Main(string[] args)
        {{
            var builder = WebApplication.CreateBuilder(args);
            
            builder.Services.AddControllers();
            builder.Services.AddDbContext<AppDbContext>(options =>
                options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
            
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();
            
            var app = builder.Build();
            
            if (app.Environment.IsDevelopment())
            {{
                app.UseSwagger();
                app.UseSwaggerUI();
            }}
            
            app.UseAuthorization();
            app.MapControllers();
            app.Run();
        }}
    }}
    
    // Models/User.cs
    [Table("users")]
    public class User
    {{
        [Key]
        [Column("org_user_id")]
        public string OrgUserId {{ get; set; }}
        
        [Column("org_id")]
        [Required]
        public string OrgId {{ get; set; }}
        
        [Required]
        [Column("name")]
        public string Name {{ get; set; }}
        
        [Column("contact_no")]
        public string ContactNo {{ get; set; }}
        
        [Column("employee_code")]
        public string EmployeeCode {{ get; set; }}
        
        [Column("created_date")]
        public DateTime CreatedDate {{ get; set; }} = DateTime.UtcNow;
        
        [Column("valid_till")]
        public DateTime ValidTill {{ get; set; }}
    }}
    
    // Data/AppDbContext.cs
    public class AppDbContext : DbContext
    {{
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) {{ }}
        
        public DbSet<User> Users {{ get; set; }}
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {{
            modelBuilder.Entity<User>()
                .HasKey(u => u.OrgUserId);
        }}
    }}
    
    // Controllers/UserController.cs
    [ApiController]
    [Route("api/org/{{orgId}}/users")]
    public class UserController : ControllerBase
    {{
        private readonly AppDbContext _context;
        
        public UserController(AppDbContext context)
        {{
            _context = context;
        }}
        
        // POST: Create User
        [HttpPost]
        public async Task<ActionResult<User>> CreateUser(string orgId, [FromBody] User user)
        {{
            user.OrgId = orgId;
            user.CreatedDate = DateTime.UtcNow;
            
            _context.Users.Add(user);
            await _context.SaveChangesAsync();
            
            return CreatedAtAction(nameof(GetUser), new {{ orgId, userId = user.OrgUserId }}, user);
        }}
        
        // GET: Get User by ID
        [HttpGet("{{userId}}")]
        public async Task<ActionResult<User>> GetUser(string orgId, string userId)
        {{
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.OrgUserId == userId && u.OrgId == orgId);
            
            if (user == null)
            {{
                return NotFound(new {{ error = "User not found" }});
            }}
            
            return Ok(user);
        }}
        
        // PUT: Update User
        [HttpPut("{{userId}}")]
        public async Task<ActionResult<User>> UpdateUser(string orgId, string userId, [FromBody] User updatedUser)
        {{
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.OrgUserId == userId && u.OrgId == orgId);
            
            if (user == null)
            {{
                return NotFound(new {{ error = "User not found" }});
            }}
            
            user.Name = updatedUser.Name;
            user.ContactNo = updatedUser.ContactNo;
            user.EmployeeCode = updatedUser.EmployeeCode;
            user.ValidTill = updatedUser.ValidTill;
            
            await _context.SaveChangesAsync();
            
            return Ok(new {{ message = "User updated", user }});
        }}
        
        // DELETE: Delete User
        [HttpDelete("{{userId}}")]
        public async Task<ActionResult> DeleteUser(string orgId, string userId)
        {{
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.OrgUserId == userId && u.OrgId == orgId);
            
            if (user == null)
            {{
                return NotFound(new {{ error = "User not found" }});
            }}
            
            _context.Users.Remove(user);
            await _context.SaveChangesAsync();
            
            return Ok(new {{ message = "User deleted" }});
        }}
    }}
}}

// appsettings.json
/*
{{
  "ConnectionStrings": {{
    "DefaultConnection": "Host=localhost;Database={org_name.lower()};Username=admin;Password=password"
  }},
  "Logging": {{
    "LogLevel": {{
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }}
  }}
}}
*/
"""


def get_code_for_language(language: str, org_id: str, org_name: str) -> dict:
    """
    Main function to get code in specified language
    """
    language_map = {
        "python": {
            "generator": lambda: generate_python_fastapi_code(org_id, org_name),
            "extension": ".py",
            "mime_type": "text/x-python",
        },
        "java": {
            "generator": lambda: generate_java_spring_code(org_id, org_name),
            "extension": ".java",
            "mime_type": "text/x-java",
        },
        "javascript": {
            "generator": lambda: generate_nodejs_express_code(org_id, org_name),
            "extension": ".js",
            "mime_type": "text/javascript",
        },
        "csharp": {
            "generator": lambda: generate_csharp_dotnet_code(org_id, org_name),
            "extension": ".cs",
            "mime_type": "text/x-csharp",
        },
    }

    if language.lower() not in language_map:
        return {
            "error": f"Language '{language}' not supported",
            "supported_languages": list(language_map.keys()),
        }

    lang_config = language_map[language.lower()]

    return {
        "code": lang_config["generator"](),
        "extension": lang_config["extension"],
        "mime_type": lang_config["mime_type"],
        "language": language,
    }


def generate_python_fastapi_code(org_id: str, org_name: str) -> str:
    """Generate Python FastAPI code (your existing code)"""
    return f"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User, UserDB
from auth import create_access_token, verify_token

Base.metadata.create_all(bind=engine)
app = FastAPI(title="{org_name} CRUD API")

@app.post("/api/org/{org_id}/users/")
def create_user(user: User, db: Session = Depends(get_db), token_data: dict = Depends(verify_token)):
    if token_data["org_id"] != "{org_id}" or token_data["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    user_db = UserDB(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@app.get("/api/org/{org_id}/users/{{user_id}}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter_by(org_user_id=user_id, org_id="{org_id}").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""
