
void FUN__text__00437c90(void *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_1,0,0xec);
  *(undefined2 *)((int)param_1 + 0x1e) = 0;
  *(undefined2 *)((int)param_1 + 0x20) = 0;
  *(undefined1 *)((int)param_1 + 0x1c) = 0xff;
  *(undefined1 *)((int)param_1 + 0x1d) = 0xff;
  *(undefined2 *)((int)param_1 + 0x18) = 0xffff;
  *(undefined2 *)((int)param_1 + 0x1a) = 0xffff;
  local_8 = 0x437cff;
  FUN__text__0056ce80();
  return;
}

