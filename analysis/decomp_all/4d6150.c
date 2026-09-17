
void __thiscall FUN__text__004d6150(undefined4 *param_1,undefined4 param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 local_4c [16];
  undefined2 local_c;
  undefined4 *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(undefined2 *)((int)param_1 + 10);
  *(short *)((int)param_1 + 10) = *(short *)((int)param_1 + 10) + 1;
  local_8 = param_1;
  FUN__text__004077c0(DAT_007a49fc);
  uVar5 = 2;
  uVar4 = *local_8;
  uVar1 = FUN__text__004142b0(uVar4,param_2,2);
  FUN__text__00408e30(uVar1,uVar4,param_2,uVar5);
  if (199 < *(short *)((int)local_8 + 10)) {
    *(undefined2 *)((int)local_8 + 10) = 199;
  }
  *(short *)((int)local_8 + 6) = *(short *)((int)local_8 + 10) - *(short *)(local_8 + 2);
  if (*(short *)((int)local_8 + 6) < 0) {
    *(undefined2 *)((int)local_8 + 6) = 0;
  }
  local_8 = (undefined4 *)0x4d6228;
  FUN__text__0056ce80();
  return;
}

