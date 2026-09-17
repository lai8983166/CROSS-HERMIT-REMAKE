
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00470620(int param_1,int param_2,int param_3,int param_4)

{
  int iVar1;
  undefined4 *puVar2;
  float10 fVar3;
  undefined4 local_5c [16];
  float local_1c;
  float local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_3 - param_1;
  local_10 = param_4 - param_2;
  fVar3 = (float10)FUN__text__005711b0((double)local_10,(double)local_c);
  local_18 = (float)fVar3;
  local_1c = (float)(fVar3 / (float10)_DAT_00592778);
  if (local_1c < _DAT_005924c0) {
    local_1c = local_1c + _DAT_0059c670 + _DAT_0059c670;
  }
  local_14 = __ftol();
  local_8 = 0x4706bc;
  FUN__text__0056ce80();
  return;
}

