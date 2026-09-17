
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0046c120(int param_1,short param_2,short param_3)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  float10 fVar4;
  undefined4 local_70 [16];
  int local_30;
  int local_2c;
  int local_28;
  short local_24;
  float local_20;
  float local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_70;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  uVar1 = *(ushort *)(*(int *)(param_1 + 600) + 2);
  local_28 = uVar1 - 0x183;
  switch(uVar1) {
  case 0x183:
  case 0x184:
  case 0x185:
  case 0x186:
  case 0x187:
  case 0x188:
  case 0x189:
  case 0x18a:
  case 0x18b:
  case 0x18c:
  case 0x18d:
  case 0x18e:
  case 399:
  case 400:
  case 0x191:
  case 0x192:
  case 0x193:
  case 0x194:
  case 0x195:
  case 0x196:
  case 0x19b:
  case 0x19c:
  case 0x19d:
  case 0x19e:
    FUN__text__0046c290();
    break;
  default:
    local_c = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
    local_10 = (short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
    local_14 = param_2;
    local_18 = param_3;
    local_2c = (int)param_2 - (int)local_c;
    local_30 = (int)param_3 - (int)local_10;
    fVar4 = (float10)FUN__text__005711b0((double)local_30,(double)local_2c);
    local_1c = (float)fVar4;
    local_20 = (float)(fVar4 / (float10)_DAT_00592778);
    if (local_20 < _DAT_005924c0) {
      local_20 = local_20 + _DAT_0059c670 + _DAT_0059c670;
    }
    local_24 = __ftol();
    local_24 = local_24 % 0x168;
    FUN__text__0046c040(param_1,CONCAT31((int3)((uint)((int)local_24 % 0x17) >> 8),
                                         (&DAT_00618768)[(int)local_24 / 0x17]));
  }
  local_8 = 0x46c25d;
  FUN__text__0056ce80();
  return;
}

