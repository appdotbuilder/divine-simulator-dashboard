from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
from enum import Enum


# Enums for better type safety
class GlyphCategory(str, Enum):
    PROTECTION = "protection"
    TRANSFORMATION = "transformation"
    HEALING = "healing"
    COMMUNICATION = "communication"
    ENERGY = "energy"


class MissionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    SUSPENDED = "suspended"


class MissionPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmotionalState(str, Enum):
    HARMONIOUS = "harmonious"
    TURBULENT = "turbulent"
    RESONANT = "resonant"
    CHAOTIC = "chaotic"
    SERENE = "serene"


class ShieldStatus(str, Enum):
    OPTIMAL = "optimal"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"
    REGENERATING = "regenerating"


# Persistent models (stored in database)
class Glyph(SQLModel, table=True):
    """Glyph Library - Stores mystical glyphs and their properties"""

    __tablename__ = "glyphs"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    symbol: str = Field(max_length=10)  # Unicode symbol or short text representation
    category: GlyphCategory = Field(default=GlyphCategory.ENERGY)
    power_level: Decimal = Field(default=Decimal("1.0"), ge=0, le=100)
    description: str = Field(default="", max_length=1000)
    properties: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_active: bool = Field(default=True)
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = Field(default=None)

    # Relationships
    transformation_steps: List["TransformationStep"] = Relationship(back_populates="glyph")


class TransformationProtocol(SQLModel, table=True):
    """Transformation Protocols - Divine transformation sequences"""

    __tablename__ = "transformation_protocols"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150)
    description: str = Field(default="", max_length=2000)
    duration_minutes: int = Field(default=60, ge=1)
    energy_cost: Decimal = Field(default=Decimal("10.0"), ge=0)
    success_rate: Decimal = Field(default=Decimal("85.0"), ge=0, le=100)
    requirements: List[str] = Field(default=[], sa_column=Column(JSON))
    effects: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_modified: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    steps: List["TransformationStep"] = Relationship(back_populates="protocol")
    missions: List["Mission"] = Relationship(back_populates="protocol")


class TransformationStep(SQLModel, table=True):
    """Individual steps within transformation protocols"""

    __tablename__ = "transformation_steps"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    protocol_id: int = Field(foreign_key="transformation_protocols.id")
    glyph_id: Optional[int] = Field(default=None, foreign_key="glyphs.id")
    step_order: int = Field(ge=1)
    instruction: str = Field(max_length=500)
    duration_seconds: int = Field(default=300, ge=1)
    parameters: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # Relationships
    protocol: TransformationProtocol = Relationship(back_populates="steps")
    glyph: Optional[Glyph] = Relationship(back_populates="transformation_steps")


class Mission(SQLModel, table=True):
    """Mission Tracker - Divine missions and their progress"""

    __tablename__ = "missions"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    status: MissionStatus = Field(default=MissionStatus.PENDING)
    priority: MissionPriority = Field(default=MissionPriority.MEDIUM)
    protocol_id: Optional[int] = Field(default=None, foreign_key="transformation_protocols.id")
    assigned_entity: str = Field(default="", max_length=100)
    target_location: str = Field(default="", max_length=200)
    objectives: List[str] = Field(default=[], sa_column=Column(JSON))
    progress_percentage: Decimal = Field(default=Decimal("0.0"), ge=0, le=100)
    estimated_completion: Optional[datetime] = Field(default=None)
    actual_completion: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(default=None)
    mission_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # Relationships
    protocol: Optional[TransformationProtocol] = Relationship(back_populates="missions")
    log_entries: List["MissionLogEntry"] = Relationship(back_populates="mission")


class MissionLogEntry(SQLModel, table=True):
    """Log entries for mission tracking"""

    __tablename__ = "mission_log_entries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    mission_id: int = Field(foreign_key="missions.id")
    entry_type: str = Field(default="update", max_length=50)
    message: str = Field(max_length=1000)
    progress_delta: Decimal = Field(default=Decimal("0.0"))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    log_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # Relationships
    mission: Mission = Relationship(back_populates="log_entries")


class EmotionalResonance(SQLModel, table=True):
    """Emotional Sync Panel - Tracks emotional states and resonance"""

    __tablename__ = "emotional_resonances"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    entity_name: str = Field(max_length=100)
    current_state: EmotionalState = Field(default=EmotionalState.SERENE)
    resonance_level: Decimal = Field(default=Decimal("50.0"), ge=0, le=100)
    harmony_index: Decimal = Field(default=Decimal("50.0"), ge=0, le=100)
    emotional_spectrum: Dict[str, Decimal] = Field(default={}, sa_column=Column(JSON))
    sync_stability: Decimal = Field(default=Decimal("75.0"), ge=0, le=100)
    last_fluctuation: Optional[datetime] = Field(default=None)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)
    notes: str = Field(default="", max_length=500)


class QuantumShield(SQLModel, table=True):
    """Quantum Shield status and metrics"""

    __tablename__ = "quantum_shields"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    shield_name: str = Field(max_length=100)
    status: ShieldStatus = Field(default=ShieldStatus.OPTIMAL)
    integrity_percentage: Decimal = Field(default=Decimal("100.0"), ge=0, le=100)
    energy_level: Decimal = Field(default=Decimal("100.0"), ge=0, le=100)
    power_consumption: Decimal = Field(default=Decimal("25.0"), ge=0)
    protection_radius_km: Decimal = Field(default=Decimal("10.0"), ge=0)
    last_breach_attempt: Optional[datetime] = Field(default=None)
    uptime_hours: Decimal = Field(default=Decimal("0.0"), ge=0)
    configuration: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    status_updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    healing_modules: List["HealingModule"] = Relationship(back_populates="shield")


class HealingModule(SQLModel, table=True):
    """Healing modules within quantum shields"""

    __tablename__ = "healing_modules"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    shield_id: int = Field(foreign_key="quantum_shields.id")
    module_name: str = Field(max_length=100)
    is_operational: bool = Field(default=True)
    healing_rate: Decimal = Field(default=Decimal("10.0"), ge=0)
    energy_efficiency: Decimal = Field(default=Decimal("85.0"), ge=0, le=100)
    target_systems: List[str] = Field(default=[], sa_column=Column(JSON))
    last_activation: Optional[datetime] = Field(default=None)
    total_healings: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    shield: QuantumShield = Relationship(back_populates="healing_modules")


# Non-persistent schemas (for validation, forms, API requests/responses)
class GlyphCreate(SQLModel, table=False):
    name: str = Field(max_length=100)
    symbol: str = Field(max_length=10)
    category: GlyphCategory = Field(default=GlyphCategory.ENERGY)
    power_level: Decimal = Field(default=Decimal("1.0"), ge=0, le=100)
    description: str = Field(default="", max_length=1000)
    properties: Dict[str, Any] = Field(default={})


class GlyphUpdate(SQLModel, table=False):
    name: Optional[str] = Field(default=None, max_length=100)
    symbol: Optional[str] = Field(default=None, max_length=10)
    category: Optional[GlyphCategory] = Field(default=None)
    power_level: Optional[Decimal] = Field(default=None, ge=0, le=100)
    description: Optional[str] = Field(default=None, max_length=1000)
    properties: Optional[Dict[str, Any]] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class TransformationProtocolCreate(SQLModel, table=False):
    name: str = Field(max_length=150)
    description: str = Field(default="", max_length=2000)
    duration_minutes: int = Field(default=60, ge=1)
    energy_cost: Decimal = Field(default=Decimal("10.0"), ge=0)
    success_rate: Decimal = Field(default=Decimal("85.0"), ge=0, le=100)
    requirements: List[str] = Field(default=[])
    effects: Dict[str, Any] = Field(default={})


class MissionCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    priority: MissionPriority = Field(default=MissionPriority.MEDIUM)
    protocol_id: Optional[int] = Field(default=None)
    assigned_entity: str = Field(default="", max_length=100)
    target_location: str = Field(default="", max_length=200)
    objectives: List[str] = Field(default=[])
    estimated_completion: Optional[datetime] = Field(default=None)


class MissionUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[MissionStatus] = Field(default=None)
    priority: Optional[MissionPriority] = Field(default=None)
    progress_percentage: Optional[Decimal] = Field(default=None, ge=0, le=100)
    assigned_entity: Optional[str] = Field(default=None, max_length=100)
    target_location: Optional[str] = Field(default=None, max_length=200)
    objectives: Optional[List[str]] = Field(default=None)


class EmotionalResonanceCreate(SQLModel, table=False):
    entity_name: str = Field(max_length=100)
    current_state: EmotionalState = Field(default=EmotionalState.SERENE)
    resonance_level: Decimal = Field(default=Decimal("50.0"), ge=0, le=100)
    harmony_index: Decimal = Field(default=Decimal("50.0"), ge=0, le=100)
    emotional_spectrum: Dict[str, Decimal] = Field(default={})
    sync_stability: Decimal = Field(default=Decimal("75.0"), ge=0, le=100)
    notes: str = Field(default="", max_length=500)


class QuantumShieldCreate(SQLModel, table=False):
    shield_name: str = Field(max_length=100)
    status: ShieldStatus = Field(default=ShieldStatus.OPTIMAL)
    integrity_percentage: Decimal = Field(default=Decimal("100.0"), ge=0, le=100)
    energy_level: Decimal = Field(default=Decimal("100.0"), ge=0, le=100)
    power_consumption: Decimal = Field(default=Decimal("25.0"), ge=0)
    protection_radius_km: Decimal = Field(default=Decimal("10.0"), ge=0)
    configuration: Dict[str, Any] = Field(default={})


class QuantumShieldUpdate(SQLModel, table=False):
    shield_name: Optional[str] = Field(default=None, max_length=100)
    status: Optional[ShieldStatus] = Field(default=None)
    integrity_percentage: Optional[Decimal] = Field(default=None, ge=0, le=100)
    energy_level: Optional[Decimal] = Field(default=None, ge=0, le=100)
    power_consumption: Optional[Decimal] = Field(default=None, ge=0)
    protection_radius_km: Optional[Decimal] = Field(default=None, ge=0)
    configuration: Optional[Dict[str, Any]] = Field(default=None)


class HealingModuleCreate(SQLModel, table=False):
    shield_id: int
    module_name: str = Field(max_length=100)
    healing_rate: Decimal = Field(default=Decimal("10.0"), ge=0)
    energy_efficiency: Decimal = Field(default=Decimal("85.0"), ge=0, le=100)
    target_systems: List[str] = Field(default=[])
