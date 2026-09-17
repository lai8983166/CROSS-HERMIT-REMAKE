
void __thiscall FUN__text__004ce090(int param_1,uint param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  char local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = *(char *)(param_1 + 5 + (param_2 & 0xffff) * 0x1c8);
  local_8 = param_1;
  if (local_10 == '\x02') {
    local_c = *(undefined4 *)(param_1 + 0xc + (param_2 & 0xffff) * 0x1c8);
    FUN__text__00428ad0(local_c);
    *(undefined1 *)(local_8 + 5 + (param_2 & 0xffff) * 0x1c8) = 0;
  }
  *(undefined1 *)(local_8 + 4 + (param_2 & 0xffff) * 0x1c8) = 0;
  FUN__text__004cd8d0(0);
  local_8 = 0x4ce13e;
  FUN__text__0056ce80();
  return;
}

