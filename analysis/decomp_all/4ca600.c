
void FUN__text__004ca600(short param_1,short param_2,uint param_3,undefined2 param_4,
                        undefined2 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  uint local_c;
  undefined *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = (&PTR_DAT_00624834)[param_3 & 0xffff];
  local_c = local_c & 0xffff0000;
  while (*(short *)(local_8 + (local_c & 0xffff) * 0xc) != -1) {
    FUN__text__004cbdb0((int)param_1 + (int)*(short *)(local_8 + (local_c & 0xffff) * 0xc),
                        (int)param_2 + (int)*(short *)(local_8 + (local_c & 0xffff) * 0xc + 2),
                        param_4,0xffffffff,param_5,
                        (int)*(short *)(local_8 + (local_c & 0xffff) * 0xc + 4),
                        (int)*(short *)(local_8 + (local_c & 0xffff) * 0xc + 6),
                        (int)*(short *)(local_8 + (local_c & 0xffff) * 0xc + 8),
                        (int)*(short *)(local_8 + (local_c & 0xffff) * 0xc + 10),0x14,0);
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = (undefined *)0x4ca70e;
  FUN__text__0056ce80();
  return;
}

