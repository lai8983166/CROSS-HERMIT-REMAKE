
undefined4 * FUN__text1__00835b18(int param_1)

{
  undefined4 *puVar1;
  int local_c;
  undefined4 *local_8;
  
  puVar1 = operator_new(0x400);
  if (param_1 == 0) {
    *puVar1 = 0x90c00ac4;
    puVar1[1] = 0x80;
    *(undefined2 *)(puVar1 + 2) = 1;
    *(undefined2 *)((int)puVar1 + 10) = 0;
    *(undefined2 *)(puVar1 + 3) = 0;
    *(undefined2 *)((int)puVar1 + 0xe) = 0x7b;
    *(undefined2 *)(puVar1 + 4) = 0x22;
    *(undefined2 *)((int)puVar1 + 0x12) = 0;
    *(undefined2 *)(puVar1 + 5) = 0;
    *(undefined2 *)((int)puVar1 + 0x16) = 0;
    *(undefined2 *)(puVar1 + 6) = 8;
    local_8 = (undefined4 *)((int)puVar1 + 0x1a);
    for (local_c = 0; *(short *)(PTR_u_MS_Sans_Serif_0086e6f4 + local_c * 2) != 0;
        local_c = local_c + 1) {
      *(undefined2 *)local_8 = *(undefined2 *)(PTR_u_MS_Sans_Serif_0086e6f4 + local_c * 2);
      local_8 = (undefined4 *)((int)local_8 + 2);
    }
    *(undefined2 *)local_8 = 0;
    for (local_8 = (undefined4 *)((int)local_8 + 2); (uint)local_8 % 4 != 0;
        local_8 = (undefined4 *)((int)local_8 + 1)) {
      *(undefined1 *)local_8 = 0;
    }
    *local_8 = 0x50801281;
    local_8[1] = 0;
    *(undefined2 *)(local_8 + 2) = 0;
    *(undefined2 *)((int)local_8 + 10) = 0;
    *(undefined2 *)(local_8 + 3) = 0x7b;
    *(undefined2 *)((int)local_8 + 0xe) = 0x22;
    *(undefined2 *)(local_8 + 4) = 0x3ea;
    *(undefined2 *)((int)local_8 + 0x12) = 0xffff;
    *(undefined2 *)(local_8 + 5) = 0x82;
    *(undefined2 *)((int)local_8 + 0x16) = 0;
    *(undefined2 *)(local_8 + 6) = 0;
  }
  else {
    FUN__text1__00848476(puVar1);
    puVar1 = (undefined4 *)0x0;
  }
  return puVar1;
}

