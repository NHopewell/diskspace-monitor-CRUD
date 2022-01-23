# DISKSPACE MONITOR API

The Diskspace Monitor API is a RESTful API which is build around **3 CORE RESOURCES**.

## System Component

<table border="0">
<tr>
<td width="40%">   
<p> An SystemComponent represents a component of the build system we would like to
monitor. A SystemComponent is created on the monitoring system (with a name and
available storage) any time an agent registered a new component in the system.</p>

<p>An example of an Agent might be a CrashDumpStore with 400G of storage.</p>

</td>

<td width="60%"> 
<strong>endpoints</strong>

|        |                           |                           |
| ------ | ------------------------- | ------------------------- |
| POST   | /v1/system_components     | Create System Component   |
| GET    | /v1/system_components/:id | Retrieve System Component |
| POST   | /v1/system_components/:id | Update System Component   |
| DELETE | /v1/system_components/:id | Delete System Component   |
| GET    | /v1/system_components     | List System Components    |

</td>
</tr>
</table>

**The System Component Object**:

<table border="0">
<tr>
<td width="40%" vertical-align="top">  
<p><strong>id</strong>: unique identifier for the object.</p>

<p><strong>name</strong>: unique name for the system component.</p>

<p><strong>total_available_storage</strong>: the total storage (in Gigabits) available to the component.</p>

<p><strong>storage_limit</strong>: the upper limit on current storage useage (as a percentage of 100).</p>

<p><strong>current_storage_useage</strong>: the amount of the components storage (in Gigabits) currently being used.</p>

</td>

<td width="60%">

```json
{
  "id": "comp_1032HU2eZvKYlo2CEPtcnUvl",
  "object": "system_component",
  "name": "CrashDumpStore",
  "total_available_storage": 400,
  "storage_limit": 90,
  "current_storage_useage": 0
}
```

</td>
</tr>
</table>

<br />

---

<br />

## Component Events

<table border="0">
<tr>
<td width="40%">   
<p>A ComponentEvent is a data point of a given SystemComponents storage
useage one moment in time. These are automatically generated when new components are registered
and the storage limits and useages change.</p>

</td>

<td width="60%"> 
<strong>endpoints</strong>

|     |                                  |                                                       |
| --- | -------------------------------- | ----------------------------------------------------- |
| GET | /v1/component_events/:id         | Retrieve latestest reported useage for a component    |
| GET | /v1/component_events/:id/history | Retrieve historic reported useages for a component    |
| GET | /v1/component_components         | Retrieve latestest reported useage for all components |

</td>
</tr>
</table>

**Component Event Object**:

<table border="0">
<tr>
    <td width="40%">   
        <p><strong>id</strong>: unique identifier for the object.</p>
        <p><strong>timestamp</strong>: the date and time at which the event was captured.</p>
        <p><strong>system_component</strong>: a nested SystemComponent object including all details about the compnent at the timestamp.</p>
    </td>

<td width="60%">

```json
{
  "id": "eve_AJ6yY15pe9xOZe",
  "object": "component_event",
  "timestamp": 1642887447,
    "system_component": {
        "id": "comp_1032HU2eZvKYlo2CEPtcnUvl",
        "name": "CrashDumpStore",
        "total_available_storage": 400,
        "storage_limit": 90,
        "current_storage_useage": 100
    }
}
```

</td>

</tr>
</table>

<br />

---

<br />

### Resource Warnings

<table border="0">
<tr>
<td width="40%">   
<p>A ResourceWarning is a warning registered when a SystemComponent
    reports a storage useage above, or close to, its upper limit.</p>

</td>

<td width="60%"> 
<strong>endpoints</strong>

|     |                       |                            |
| --- | --------------------- | -------------------------- |
| GET | /v1/resource_warnings | List all resource warnings |

</td>
</tr>
</table>

**Resource Warning Object**:

<table border="0">
<tr>
<td width="40%" vertical-align="top">  
<p><strong>id</strong>: unique identifier for the object.</p>

<p><strong>warning_type</strong>: the type of warning issued by the system (out of memory or close to memory limit).</p>

<p><strong>component_event</strong>: a nested ComponentEvent object holding a SystemComponent object at a given timestamp.</p>

</td>

<td width="60%">

```json
{
  "id": "warn_ErTsH2eZvKYlo2CI7ukc",
  "object": "resource_warning",
  "warning_type": "over_memory_limit",
  "component_event": {
        "id": "eve_AJ6yY15pe9xOZe",
        "timestamp": 2342887447,
        "system_component": {
            "id": "comp_1032HU2eZvKYlo2CEPtcnUvl",
            "name": "CrashDumpStore",
            "total_available_storage": 400,
            "storage_limit": 90,
            "current_storage_useage": 395
            }
    }
}
```

</td>
</tr>
</table>
