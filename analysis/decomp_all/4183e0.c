
void FUN__text__004183e0(undefined4 param_1)

{
  int iVar1;
  char *pcVar2;
  undefined4 *puVar3;
  undefined4 local_88 [16];
  int local_48;
  int local_44;
  undefined4 local_38 [12];
  undefined4 *local_8;
  
  puVar3 = local_88;
  for (iVar1 = 0x21; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  pcVar2 = "Internet TCP/IP Connection For DirectPlay";
  puVar3 = local_38;
  for (iVar1 = 10; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = *(undefined4 *)pcVar2;
    pcVar2 = pcVar2 + 4;
    puVar3 = puVar3 + 1;
  }
  *(undefined2 *)puVar3 = *(undefined2 *)pcVar2;
  local_44 = FUN__text__004184a0(param_1);
  if (local_44 == 0) {
    (**(code **)(*(int *)*local_8 + 0x98))(*local_8,local_8[2],0);
    local_48 = FUN__text__0056ce80();
    local_44 = local_48;
    if ((local_48 != -0x7788fffb) && (local_48 != 0)) {
      FUN__text__0041b4a0(local_48);
    }
  }
  local_8 = (undefined4 *)0x418496;
  FUN__text__0056ce80();
  return;
}

