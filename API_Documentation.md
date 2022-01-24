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

|        |                             |                           |
| ------ | --------------------------- | ------------------------- |
| POST   | /v1/system_components       | Create System Component   |
| GET    | /v1/system_components/:name | Retrieve System Component |
| PATCH  | /v1/system_components/:name | Update System Component   |
| DELETE | /v1/system_components/:name | Delete System Component   |
| GET    | /v1/system_components       | List System Components    |

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
  "id": 1,
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

|     |                                    |                                         |
| --- | ---------------------------------- | --------------------------------------- |
| GET | /v1/component_events/:name         | Get latestest useage for component      |
| GET | /v1/component_events/:name/history | Get historic useages for component      |
| GET | /v1/component_components           | Get latestest useage for all components |

</td>
</tr>
</table>

**Component Event Object**:

<table border="0">
<tr>
    <td width="40%">   
        <p><strong>id</strong>: unique identifier for the object.</p>
        <p><strong>timestamp</strong>: the date and time at which the event was captured.</p>
        <p><strong>component_snapshot</strong>: a nested SystemComponent object including all details about the compnent at the timestamp of the event.</p>
    </td>

<td width="60%">

```json
{
  "event_id": "ecaac8db-e9de-4eb8-b445-a4f5bb00bb0e",
  "timestamp": "01.23.2022 22:36:27",
  "component_snapshot": {
    "component_name": "CrashDump",
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

## Resource Warnings

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
  "warning_id": "4dc9a9af-d050-42a5-a1c6-ccf11f9b5e84",
  "warning_type": "over memory limit",
  "component_event": {
    "event_id": "8ac60ebf-eb1d-4277-b293-accccc8b252f",
    "timestamp": "01.23.2022 23:41:11",
    "component_snapshot": {
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
