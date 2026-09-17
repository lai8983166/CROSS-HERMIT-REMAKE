
void __fastcall FUN__text__004cade0(int param_1)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined2 *)(param_1 + 0x16) = 0;
  local_c = local_c & 0xffff0000;
  local_8 = param_1;
  while ((local_c & 0xffff) < 10) {
    *(undefined2 *)(local_8 + 0x18 + (local_c & 0xffff) * 0x110) = 0;
    *(undefined2 *)(local_8 + 0x1a + (local_c & 0xffff) * 0x110) = 0;
    uVar1 = FUN__text__004cafa0();
    *(undefined2 *)(local_8 + 0x1c + (local_c & 0xffff) * 0x110) = uVar1;
    *(undefined2 *)(local_8 + 0x1e + (local_c & 0xffff) * 0x110) = 0;
    uVar1 = FUN__text__004cb080();
    *(undefined2 *)(local_8 + 0x20 + (local_c & 0xffff) * 0x110) = uVar1;
    *(undefined2 *)(local_8 + 0x24 + (local_c & 0xffff) * 0x110) = 0;
    *(undefined2 *)(local_8 + 0x22 + (local_c & 0xffff) * 0x110) = 0;
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4caefd;
  FUN__text__0056ce80();
  return;
}

