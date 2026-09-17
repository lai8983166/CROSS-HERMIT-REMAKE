
void __thiscall FUN__text__0040d970(undefined4 *param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *param_1 = param_2;
  local_8 = param_1;
  uVar1 = FUN__text__004142b0();
  local_8[1] = uVar1;
  local_8 = (undefined4 *)0x40d9b4;
  FUN__text__0056ce80();
  return;
}

