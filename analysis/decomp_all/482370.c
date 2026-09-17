
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00482370(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  float10 fVar3;
  undefined4 local_68 [16];
  float local_28;
  float local_24;
  float local_20;
  float local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_1c = _DAT_0059d918 / (float)*(int *)(param_1 + 0x108b50);
  local_8 = param_1;
  for (local_c = 0; local_c != *(int *)(local_8 + 0x108b50); local_c = local_c + 1) {
    iVar1 = __ftol();
    local_18 = (iVar1 + *(short *)(param_2 + 2)) % 0x168;
    local_20 = (float)local_18 * _DAT_00592778;
    fVar3 = (float10)FUN__text__0056d9d4((double)(_DAT_00618ea8 * local_20));
    local_24 = (float)(fVar3 * (float10)_DAT_00618eb0);
    fVar3 = (float10)FUN__text__0056d924((double)(_DAT_00618eac * local_20));
    local_28 = (float)(fVar3 * (float10)_DAT_00618eb4);
    local_10 = __ftol();
    local_10 = local_10 + *(short *)(param_2 + 8);
    local_14 = __ftol();
    local_14 = local_14 + *(short *)(param_2 + 10);
    FUN__text__0046df90(*(undefined4 *)(local_8 + 0x108b60 + local_c * 4),local_10,local_14,1);
  }
  local_8 = 0x48248e;
  FUN__text__0056ce80();
  return;
}

